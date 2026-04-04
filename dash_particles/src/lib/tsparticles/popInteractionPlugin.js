class PopInteractionInstance {
    constructor(container) {
        this.container = container;
    }

    handleClickMode(mode) {
        if (mode !== 'pop') {
            return;
        }

        const clickPosition = this.container?.interactivity?.mouse?.clickPosition;

        if (!clickPosition) {
            return;
        }

        const radius = this.container?.retina?.pixelRatio || 1;
        const quadTree = this.container?.particles?.quadTree;

        if (!quadTree || typeof quadTree.queryCircle !== 'function') {
            return;
        }

        const poppedParticles = quadTree.queryCircle(clickPosition, radius);

        if (!poppedParticles?.length) {
            return;
        }

        for (const particle of poppedParticles) {
            this.container.particles.remove(particle);
        }
    }

    clear() {}

    init() {}

    interact() {}

    isEnabled() {
        return true;
    }

    reset() {}
}

export const loadPopInteractionPlugin = async (engine, refresh = true) => {
    await engine.addInteractor(
        'externalPop',
        (container) => Promise.resolve(new PopInteractionInstance(container)),
        refresh,
    );
};
