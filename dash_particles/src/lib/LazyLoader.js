import React, { Suspense } from 'react';
import PropTypes from 'prop-types';

const LazyDashParticles = React.lazy(
    () => import(/* webpackChunkName: "DashParticles" */ './fragments/DashParticles.react')
);

const DashParticles = (props) => {
    return (
        <Suspense fallback={null}>
            <LazyDashParticles {...props} />
        </Suspense>
    );
};

DashParticles.propTypes = {
    id: PropTypes.string,
    options: PropTypes.object,
    runtime: PropTypes.oneOf(['auto', 'basic', 'slim', 'full']),
    height: PropTypes.string,
    width: PropTypes.string,
    className: PropTypes.string,
    style: PropTypes.object,
    particlesLoaded: PropTypes.bool,
    setProps: PropTypes.func
};

export {
    DashParticles
};
