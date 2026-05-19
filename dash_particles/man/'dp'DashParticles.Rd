% Auto-generated: do not edit by hand
\name{'dp'DashParticles}

\alias{'dp'DashParticles}

\title{DashParticles component}

\description{
DashParticles renders a tsParticles canvas inside Dash.  The component automatically loads the smallest tsParticles runtime tier it can infer from the provided options, and falls back to the full runtime when a more specialized plugin is needed.
}

\usage{
'dp'DashParticles(id=NULL, className=NULL, height=NULL, options=NULL,
particlesLoaded=NULL, runtime=NULL, style=NULL, width=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{className}{Character. Additional CSS class for the container div.}

\item{height}{Character. Height of the particles container. Can be any valid CSS dimension value.}

\item{options}{Named list. tsParticles options for the canvas.}

\item{particlesLoaded}{Logical. Boolean flag indicating if particles have been loaded.
This is a read-only prop updated by the component.}

\item{runtime}{A value equal to: 'auto', 'basic', 'slim', 'full'. tsParticles runtime tier to load. Use "auto" to infer the smallest
runtime from the options, or force "basic", "slim", or "full".}

\item{style}{Named list. Additional inline styles for the container div.}

\item{width}{Character. Width of the particles container. Can be any valid CSS dimension value.}
}

\value{named list of JSON elements corresponding to React.js properties and their values}

