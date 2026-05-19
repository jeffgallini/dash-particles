import React, { useEffect, useMemo, useRef } from 'react';
import PropTypes from 'prop-types';
import { tsParticles } from '@tsparticles/engine';

const RUNTIME_AUTO = 'auto';
const RUNTIME_BASIC = 'basic';
const RUNTIME_SLIM = 'slim';
const RUNTIME_FULL = 'full';
const RUNTIME_RANK = {
    [RUNTIME_BASIC]: 1,
    [RUNTIME_SLIM]: 2,
    [RUNTIME_FULL]: 3,
};
const RUNTIME_OPTIONS = [RUNTIME_AUTO, RUNTIME_BASIC, RUNTIME_SLIM, RUNTIME_FULL];
const FULL_RUNTIME_MODES = new Set(['absorber', 'emitter', 'pop', 'trail']);
const FULL_RUNTIME_SHAPES = new Set(['char', 'character', 'multiline-text', 'text']);
const FULL_PARTICLE_KEYS = ['destroy', 'roll', 'tilt', 'twinkle', 'wobble'];
const SLIM_PARTICLE_KEYS = ['collisions', 'life', 'rotate', 'stroke'];

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

const runtimePromises = {};
let highestRuntimeRankLoaded = 0;

const hasOwn = (value, key) => (
    Boolean(value)
    && typeof value === 'object'
    && Object.prototype.hasOwnProperty.call(value, key)
);

const asArray = (value) => {
    if (Array.isArray(value)) {
        return value;
    }

    return value === undefined || value === null ? [] : [value];
};

const normalizedStringArray = (value) => (
    asArray(value)
        .filter((item) => typeof item === 'string')
        .map((item) => item.toLowerCase())
);

const collectEventModes = (options) => {
    const events = options && options.interactivity && options.interactivity.events;

    if (!events) {
        return [];
    }

    return [
        ...normalizedStringArray(events.onClick && events.onClick.mode),
        ...normalizedStringArray(events.onHover && events.onHover.mode),
        ...normalizedStringArray(events.onDiv && events.onDiv.mode),
    ];
};

const hasAnyKey = (value, keys) => keys.some((key) => hasOwn(value, key));

const detectRuntimeTier = (options) => {
    const particleOptions = (options && options.particles) || {};
    const interactivityModes = (options && options.interactivity && options.interactivity.modes) || {};
    const shapeTypes = normalizedStringArray(particleOptions.shape && particleOptions.shape.type);
    const eventModes = collectEventModes(options);

    if (
        hasOwn(options, 'absorbers')
        || hasOwn(options, 'canvasMask')
        || hasOwn(options, 'emitters')
        || hasOwn(interactivityModes, 'absorbers')
        || hasOwn(interactivityModes, 'emitters')
        || hasOwn(interactivityModes, 'trail')
        || hasAnyKey(particleOptions, FULL_PARTICLE_KEYS)
        || shapeTypes.some((shapeType) => FULL_RUNTIME_SHAPES.has(shapeType))
        || eventModes.some((mode) => FULL_RUNTIME_MODES.has(mode))
    ) {
        return RUNTIME_FULL;
    }

    if (
        (particleOptions.links && particleOptions.links.enable !== false)
        || hasAnyKey(particleOptions, SLIM_PARTICLE_KEYS)
        || shapeTypes.some((shapeType) => shapeType !== 'circle')
        || eventModes.some((mode) => mode !== 'none')
        || Boolean(options && options.interactivity && options.interactivity.events
            && options.interactivity.events.onHover
            && options.interactivity.events.onHover.parallax
            && options.interactivity.events.onHover.parallax.enable)
    ) {
        return RUNTIME_SLIM;
    }

    return RUNTIME_BASIC;
};

const normalizeRuntime = (runtime) => (
    RUNTIME_OPTIONS.includes(runtime) ? runtime : RUNTIME_AUTO
);

const resolveRuntime = (runtime, options) => {
    const normalizedRuntime = normalizeRuntime(runtime);

    return normalizedRuntime === RUNTIME_AUTO ? detectRuntimeTier(options) : normalizedRuntime;
};

const loadBasicRuntime = async () => {
    const { loadBasic } = await import(
        /* webpackChunkName: "tsparticles-basic" */ '@tsparticles/basic'
    );

    await loadBasic(tsParticles, false);
};

const loadSlimRuntime = async () => {
    const { loadSlim } = await import(
        /* webpackChunkName: "tsparticles-slim" */ '@tsparticles/slim'
    );

    await loadSlim(tsParticles, false);
};

const loadFullRuntime = async () => {
    const [
        { loadFull },
        { loadCanvasMaskPlugin },
        { loadExternalPopInteraction },
    ] = await Promise.all([
        import(/* webpackChunkName: "tsparticles-full" */ 'tsparticles'),
        import(/* webpackChunkName: "tsparticles-full" */ '@tsparticles/plugin-canvas-mask'),
        import(/* webpackChunkName: "tsparticles-full" */ '@tsparticles/interaction-external-pop'),
    ]);

    await loadFull(tsParticles, false);
    await loadExternalPopInteraction(tsParticles, false);
    await loadCanvasMaskPlugin(tsParticles, false);
};

const ensureRuntimeLoaded = async (runtime) => {
    const runtimeTier = runtime === RUNTIME_AUTO ? RUNTIME_SLIM : runtime;
    const runtimeRank = RUNTIME_RANK[runtimeTier];

    if (highestRuntimeRankLoaded >= runtimeRank) {
        return;
    }

    if (!runtimePromises[runtimeTier]) {
        runtimePromises[runtimeTier] = (async () => {
            if (runtimeTier === RUNTIME_BASIC) {
                await loadBasicRuntime();
            } else if (runtimeTier === RUNTIME_SLIM) {
                await loadSlimRuntime();
            } else {
                await loadFullRuntime();
            }

            highestRuntimeRankLoaded = Math.max(highestRuntimeRankLoaded, runtimeRank);
        })();
    }

    await runtimePromises[runtimeTier];
};

const sortObjectKeys = (value) => {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
        return value;
    }

    return Object.keys(value).sort().reduce((result, key) => {
        result[key] = value[key];
        return result;
    }, {});
};

const stableStringify = (value) => (
    JSON.stringify(value, (_key, currentValue) => sortObjectKeys(currentValue))
);

const resolveOptions = (options) => {
    if (!options) {
        return defaultOptions;
    }

    return {
        ...options,
        fullScreen: {
            ...defaultOptions.fullScreen,
            ...(options.fullScreen || {}),
        },
    };
};

const useDashOptionsLoading = () => {
    const dashApi = typeof window !== 'undefined' ? window.dash_component_api : undefined;

    if (!dashApi || !dashApi.useDashContext) {
        return false;
    }

    const dashContext = dashApi.useDashContext();

    if (!dashContext || !dashContext.useLoading) {
        return false;
    }

    return Boolean(dashContext.useLoading({
        filterFunc: (loading) => loading && loading.property === 'options',
    }));
};

const loadWithRuntimeFallback = async (containerId, options, runtime) => {
    try {
        await ensureRuntimeLoaded(runtime);
        return await tsParticles.load({ id: containerId, options });
    } catch (error) {
        if (runtime === RUNTIME_FULL) {
            throw error;
        }

        await ensureRuntimeLoaded(RUNTIME_FULL);
        return tsParticles.load({ id: containerId, options });
    }
};

const destroyParticles = (particlesInstance) => {
    if (!particlesInstance) {
        return;
    }

    try {
        particlesInstance.destroy();
    } catch (error) {
        console.error('Error destroying particles:', error);
    }
};

/**
 * DashParticles renders a tsParticles canvas inside Dash.
 *
 * The component automatically loads the smallest tsParticles runtime tier it
 * can infer from the provided options, and falls back to the full runtime when
 * a more specialized plugin is needed.
 */
const DashParticles = ({
    id,
    options,
    runtime = RUNTIME_AUTO,
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
    const lastLoadedOptionsSignature = useRef(null);
    const pausedForDashLoading = useRef(false);
    const resolvedOptionsRef = useRef(null);
    const resolvedRuntimeRef = useRef(null);
    const resolvedLoadSignatureRef = useRef(null);
    const loadSequence = useRef(0);
    const setPropsRef = useRef(setProps);
    const containerId = `${id || 'dash-particles'}-particles`;
    const optionsLoading = useDashOptionsLoading();
    const optionsSignature = stableStringify(options || null);
    const resolvedOptions = useMemo(() => resolveOptions(options), [optionsSignature]);
    const resolvedOptionsSignature = useMemo(() => stableStringify(resolvedOptions), [resolvedOptions]);
    const resolvedRuntime = useMemo(
        () => resolveRuntime(runtime, resolvedOptions),
        [runtime, resolvedOptionsSignature]
    );
    const resolvedLoadSignature = `${resolvedRuntime}:${resolvedOptionsSignature}`;

    resolvedOptionsRef.current = resolvedOptions;
    resolvedRuntimeRef.current = resolvedRuntime;
    resolvedLoadSignatureRef.current = resolvedLoadSignature;

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
        const currentSequence = loadSequence.current + 1;
        loadSequence.current = currentSequence;

        const resetAndLoadParticles = async () => {
            if (!containerRef.current) {
                return;
            }

            const currentLoadSignature = resolvedLoadSignatureRef.current;

            if (lastLoadedOptionsSignature.current === currentLoadSignature) {
                return;
            }

            destroyParticles(particlesInstance.current);
            particlesInstance.current = null;
            initialized.current = false;
            pausedForDashLoading.current = false;

            try {
                const nextParticlesInstance = await loadWithRuntimeFallback(
                    containerId,
                    resolvedOptionsRef.current,
                    resolvedRuntimeRef.current
                );

                if (cancelled || loadSequence.current !== currentSequence || !containerRef.current) {
                    destroyParticles(nextParticlesInstance);
                    return;
                }

                particlesInstance.current = nextParticlesInstance;
                initialized.current = true;
                lastLoadedOptionsSignature.current = currentLoadSignature;
                reportLoaded(true);
            } catch (error) {
                console.error('Error loading particles:', error);
                const containerNode = document.getElementById(containerId);
                if (containerNode) {
                    containerNode.textContent = 'Particles failed to initialize.';
                    containerNode.style.color = '#ef4444';
                    containerNode.style.padding = '12px';
                }
                reportLoaded(false);
            }
        };

        resetAndLoadParticles();

        return () => {
            cancelled = true;
            loadSequence.current += 1;
            destroyParticles(particlesInstance.current);
            particlesInstance.current = null;
            initialized.current = false;
            lastLoadedOptionsSignature.current = null;
            pausedForDashLoading.current = false;
            reportLoaded(false);
        };
    }, [containerId, resolvedLoadSignature]);

    useEffect(() => {
        if (!initialized.current || !particlesInstance.current) {
            return;
        }

        if (optionsLoading) {
            if (particlesInstance.current.animationStatus) {
                try {
                    particlesInstance.current.pause();
                    pausedForDashLoading.current = true;
                } catch (error) {
                    console.error('Error pausing particles:', error);
                }
            }

            return;
        }

        if (pausedForDashLoading.current) {
            try {
                particlesInstance.current.play();
                pausedForDashLoading.current = false;
            } catch (error) {
                console.error('Error resuming particles:', error);
            }
        }
    }, [optionsLoading]);

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
     */
    options: PropTypes.object,

    /**
     * tsParticles runtime tier to load. Use "auto" to infer the smallest
     * runtime from the options, or force "basic", "slim", or "full".
     */
    runtime: PropTypes.oneOf(['auto', 'basic', 'slim', 'full']),

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
