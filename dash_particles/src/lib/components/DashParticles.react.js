import React, { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import { tsParticles } from '@tsparticles/engine';
import { loadFull } from 'tsparticles';
import { loadCanvasMaskPlugin } from '@tsparticles/plugin-canvas-mask';
import { loadExternalPopInteraction } from '@tsparticles/interaction-external-pop';

const defaultOptions = {
    fullScreen: {
        enable: false,
        zIndex: 0,
    },
    background: {
        color: {
            value: 'transparent',
        },
    },
    fpsLimit: 60,
    particles: {
        color: {
            value: '#0075FF',
        },
        links: {
            color: '#0075FF',
            distance: 150,
            enable: true,
            opacity: 0.5,
            width: 1,
        },
        move: {
            direction: 'none',
            enable: true,
            outModes: {
                default: 'bounce',
            },
            random: false,
            speed: 3,
            straight: false,
        },
        number: {
            density: {
                enable: true,
                area: 800,
            },
            value: 80,
        },
        opacity: {
            value: 0.5,
        },
        shape: {
            type: 'circle',
        },
        size: {
            value: { min: 1, max: 5 },
        },
    },
    detectRetina: true,
};

let runtimePromise;

const ensureRuntimeLoaded = async () => {
    if (!runtimePromise) {
        // `loadFull` already includes the slim bundle. We register the
        // official pop/canvas-mask plugins separately so manual
        // `canvasMask` configs and `onClick.mode = "pop"` work in the
        // bundled Dash runtime as well.
        runtimePromise = (async () => {
            await loadFull(tsParticles, false);
            await loadExternalPopInteraction(tsParticles, false);
            await loadCanvasMaskPlugin(tsParticles, false);
        })();
    }

    await runtimePromise;
};

/**
 * DashParticles renders a tsParticles canvas inside Dash.
 *
 * The package currently loads the `tsparticles` full runtime bundle plus the
 * extra plugins needed for click-pop interactions, image shapes, text shapes,
 * and canvas masks.
 */
const DashParticles = ({
    id,
    options,
    height = '400px',
    width = '100%',
    className,
    style = {},
    particlesLoaded,
    setProps
}) => {
    const containerRef = useRef(null);
    const initialized = useRef(false);
    const particlesInstance = useRef(null);
    const reportedLoaded = useRef(null);
    const setPropsRef = useRef(setProps);
    const containerId = `${id || 'dash-particles'}-particles`;
    const resolvedOptions = options ? {
        ...options,
        fullScreen: {
            ...defaultOptions.fullScreen,
            ...(options.fullScreen || {}),
        },
    } : defaultOptions;

    useEffect(() => {
        setPropsRef.current = setProps;
    }, [setProps]);

    const reportLoaded = (value) => {
        if (!setPropsRef.current || reportedLoaded.current === value) {
            return;
        }

        reportedLoaded.current = value;
        setPropsRef.current({ particlesLoaded: value });
    };

    useEffect(() => {
        let cancelled = false;

        const initParticles = async () => {
            if (initialized.current || !containerRef.current) {
                return;
            }

            try {
                await ensureRuntimeLoaded();

                if (cancelled || !containerRef.current) {
                    return;
                }

                particlesInstance.current = await tsParticles.load({
                    id: containerId,
                    options: resolvedOptions,
                });

                initialized.current = true;
                reportLoaded(true);
            } catch (error) {
                console.error('Error initializing particles:', error);
                const containerNode = document.getElementById(containerId);
                if (containerNode) {
                    containerNode.textContent = 'Particles failed to initialize.';
                    containerNode.style.color = '#ef4444';
                    containerNode.style.padding = '12px';
                }
                reportLoaded(false);
            }
        };

        initParticles();

        return () => {
            cancelled = true;

            if (particlesInstance.current) {
                try {
                    particlesInstance.current.destroy();
                } catch (error) {
                    console.error('Error destroying particles:', error);
                }
            }

            particlesInstance.current = null;
            initialized.current = false;
            reportLoaded(false);
        };
    }, [containerId]);

    useEffect(() => {
        const updateParticles = async () => {
            if (!initialized.current || !particlesInstance.current) {
                return;
            }

            try {
                particlesInstance.current.options.load(resolvedOptions);
                await particlesInstance.current.refresh();
                reportLoaded(true);
            } catch (error) {
                console.error('Error updating particles:', error);
                reportLoaded(false);
            }
        };

        updateParticles();
    }, [resolvedOptions]);

    const containerStyle = {
        height,
        width,
        position: 'relative',
        ...style
    };

    return (
        <div
            id={id}
            ref={containerRef}
            className={className}
            style={containerStyle}
        >
            <div id={containerId} style={{ height: '100%', width: '100%' }} />
        </div>
    );
};

DashParticles.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * tsParticles options for the canvas.
     *
     * This package currently ships with the `tsparticles` full bundle plus the
     * click-pop, image-shape, text-shape, and canvas-mask plugins. That covers
     * examples such as Among Us and Font Awesome out of the box. More exotic
     * plugins can still require additional frontend work.
     */
    options: PropTypes.object,

    /**
     * Height of the particles container. Can be any valid CSS dimension value.
     */
    height: PropTypes.string,

    /**
     * Width of the particles container. Can be any valid CSS dimension value.
     */
    width: PropTypes.string,

    /**
     * Additional CSS class for the container div.
     */
    className: PropTypes.string,

    /**
     * Additional inline styles for the container div.
     */
    style: PropTypes.object,

    /**
     * Boolean flag indicating if particles have been loaded.
     * This is a read-only prop updated by the component.
     */
    particlesLoaded: PropTypes.bool,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default DashParticles;
