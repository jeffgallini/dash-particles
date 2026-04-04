% Auto-generated: do not edit by hand
\name{'dp'DashParticles}

\alias{'dp'DashParticles}

\title{DashParticles component}

\description{
DashParticles renders a tsParticles canvas inside Dash.  The package currently loads the `tsparticles` full runtime bundle plus the extra plugins needed for click-pop interactions, image shapes, text shapes, and canvas masks.
}

\usage{
'dp'DashParticles(id=NULL, className=NULL, height=NULL, options=NULL,
particlesLoaded=NULL, style=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{className}{Character. Additional CSS class for the container div.}

\item{height}{Character. Height of the particles container. Can be any valid CSS dimension value.}

\item{options}{Named list. tsParticles options for the canvas.

This package currently ships with the `tsparticles` full bundle plus the
click-pop, image-shape, text-shape, and canvas-mask plugins. That covers
examples such as Among Us and Font Awesome out of the box. More exotic
plugins can still require additional frontend work.}

\item{particlesLoaded}{Logical. Boolean flag indicating if particles have been loaded.
This is a read-only prop updated by the component.}

\item{style}{Named list. Additional inline styles for the container div.}

\item{width}{Character. Width of the particles container. Can be any valid CSS dimension value.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

