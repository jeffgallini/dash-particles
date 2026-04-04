const DEFAULT_POSITION = { x: 50, y: 50 };
const DEFAULT_OVERRIDE = { color: true, opacity: false };
const DEFAULT_PIXEL_OFFSET = 4;

const defaultPixelFilter = (pixel) => pixel.a > 0;

const getObject = (value) => (value && typeof value === 'object' ? value : {});

const normalizeMaskOptions = (value) => {
    const data = getObject(value);
    const override = getObject(data.override);
    const pixels = getObject(data.pixels);
    const position = getObject(data.position);

    return {
        element:
            typeof HTMLCanvasElement !== 'undefined' && data.element instanceof HTMLCanvasElement
                ? data.element
                : undefined,
        enable: Boolean(data.enable),
        image: data.image ? { ...data.image } : undefined,
        override: {
            color: override.color !== undefined ? override.color : DEFAULT_OVERRIDE.color,
            opacity: override.opacity !== undefined ? override.opacity : DEFAULT_OVERRIDE.opacity,
        },
        pixels: {
            filter: pixels.filter,
            offset: Number.isFinite(pixels.offset) ? pixels.offset : DEFAULT_PIXEL_OFFSET,
        },
        position: {
            x: Number.isFinite(position.x) ? position.x : DEFAULT_POSITION.x,
            y: Number.isFinite(position.y) ? position.y : DEFAULT_POSITION.y,
        },
        scale: Number.isFinite(data.scale) ? data.scale : 1,
        selector: typeof data.selector === 'string' ? data.selector : undefined,
    };
};

const mergeMaskOptions = (currentValue, nextValue) => {
    const current = normalizeMaskOptions(currentValue);
    const next = getObject(nextValue);

    return normalizeMaskOptions({
        ...current,
        ...next,
        override: {
            ...current.override,
            ...getObject(next.override),
        },
        pixels: {
            ...current.pixels,
            ...getObject(next.pixels),
        },
        position: {
            ...current.position,
            ...getObject(next.position),
        },
    });
};

const shuffle = (items) => {
    for (let index = items.length - 1; index > 0; index -= 1) {
        const swapIndex = Math.floor(Math.random() * (index + 1));
        [items[index], items[swapIndex]] = [items[swapIndex], items[index]];
    }

    return items;
};

const resolveParticleCount = (value, fallback) => {
    if (typeof value === 'number' && Number.isFinite(value)) {
        return value;
    }

    if (value && typeof value === 'object') {
        if (typeof value.max === 'number' && Number.isFinite(value.max)) {
            return value.max;
        }

        if (typeof value.min === 'number' && Number.isFinite(value.min)) {
            return value.min;
        }
    }

    return fallback;
};

const resolvePixelFilter = (filter) => {
    if (typeof filter === 'function') {
        return filter;
    }

    if (typeof filter === 'string' && typeof window !== 'undefined') {
        const namedFilter = window[filter];

        if (typeof namedFilter === 'function') {
            return namedFilter;
        }
    }

    return defaultPixelFilter;
};

const readCanvasPixels = (context, width, height, pixelOffset) => {
    const byteStep = Math.max(DEFAULT_PIXEL_OFFSET, Math.floor(pixelOffset || DEFAULT_PIXEL_OFFSET));
    const imageData = context.getImageData(0, 0, width, height).data;
    const pixels = [];

    for (let byteIndex = 0; byteIndex < imageData.length; byteIndex += byteStep) {
        const pixelIndex = Math.floor(byteIndex / 4);

        pixels.push({
            a: imageData[byteIndex + 3] / 255,
            b: imageData[byteIndex + 2],
            g: imageData[byteIndex + 1],
            r: imageData[byteIndex],
            x: pixelIndex % width,
            y: Math.floor(pixelIndex / width),
        });
    }

    return {
        height,
        pixels,
        width,
    };
};

const loadImagePixels = async (source, pixelOffset) => {
    const image = new Image();

    image.crossOrigin = 'Anonymous';

    await new Promise((resolve, reject) => {
        image.onload = resolve;
        image.onerror = reject;
        image.src = source;
    });

    const canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;

    const context = canvas.getContext('2d');

    if (!context) {
        throw new Error('tsParticles canvas mask plugin could not create a canvas context.');
    }

    context.drawImage(image, 0, 0, image.width, image.height);

    return readCanvasPixels(context, canvas.width, canvas.height, pixelOffset);
};

const loadCanvasElementPixels = (element, pixelOffset) => {
    const context = element.getContext('2d');

    if (!context) {
        return undefined;
    }

    return readCanvasPixels(context, element.width, element.height, pixelOffset);
};

const addParticlesFromCanvasPixels = (container, pixelData, maskOptions) => {
    const particleManager = container?.particles;

    if (!particleManager || typeof particleManager.addParticle !== 'function' || !pixelData?.pixels?.length) {
        return;
    }

    const filter = resolvePixelFilter(maskOptions?.pixels?.filter);
    const eligiblePixels = shuffle(pixelData.pixels.filter(filter));

    if (!eligiblePixels.length) {
        return;
    }

    const targetCount = resolveParticleCount(
        container?.actualOptions?.particles?.number?.value,
        eligiblePixels.length,
    );
    const particleCount = Math.min(eligiblePixels.length, targetCount);
    const scale = Number.isFinite(maskOptions?.scale) ? maskOptions.scale : 1;
    const position = maskOptions?.position || DEFAULT_POSITION;
    const canvasSize = container.canvas?.size || { height: 0, width: 0 };
    const offsetX = (canvasSize.width * position.x) / 100 - (pixelData.width * scale) / 2;
    const offsetY = (canvasSize.height * position.y) / 100 - (pixelData.height * scale) / 2;
    const override = maskOptions?.override || DEFAULT_OVERRIDE;

    for (let index = 0; index < particleCount; index += 1) {
        const pixel = eligiblePixels[index];
        const particleOptions = {};

        if (override.color) {
            particleOptions.color = {
                value: {
                    b: pixel.b,
                    g: pixel.g,
                    r: pixel.r,
                },
            };
        }

        if (override.opacity) {
            particleOptions.opacity = { value: pixel.a };
        }

        particleManager.addParticle(
            {
                x: pixel.x * scale + offsetX,
                y: pixel.y * scale + offsetY,
            },
            particleOptions,
        );
    }
};

class CanvasMaskInstance {
    constructor(container) {
        this.container = container;
    }

    async init() {
        const maskOptions = normalizeMaskOptions(this.container?.actualOptions?.canvasMask);

        if (!maskOptions.enable) {
            return;
        }

        let pixelData;

        if (maskOptions.image?.src) {
            pixelData = await loadImagePixels(maskOptions.image.src, maskOptions.pixels.offset);
        } else if (maskOptions.element) {
            pixelData = loadCanvasElementPixels(maskOptions.element, maskOptions.pixels.offset);
        } else if (maskOptions.selector) {
            const element = document.querySelector(maskOptions.selector);

            if (typeof HTMLCanvasElement !== 'undefined' && element instanceof HTMLCanvasElement) {
                pixelData = loadCanvasElementPixels(element, maskOptions.pixels.offset);
            }
        }

        addParticlesFromCanvasPixels(this.container, pixelData, maskOptions);
    }
}

class CanvasMaskPlugin {
    constructor() {
        this.id = 'canvasMask';
    }

    getPlugin(container) {
        return Promise.resolve(new CanvasMaskInstance(container));
    }

    loadOptions(options, source) {
        if (!this.needsPlugin(options) && !this.needsPlugin(source)) {
            return;
        }

        options.canvasMask = mergeMaskOptions(options.canvasMask, source?.canvasMask);
    }

    needsPlugin(options) {
        return Boolean(options?.canvasMask?.enable);
    }
}

export const loadCanvasMaskPlugin = async (engine, refresh = true) => {
    await engine.addPlugin(new CanvasMaskPlugin(), refresh);
};
