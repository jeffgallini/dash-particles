# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dpDashParticles <- function(id=NULL, className=NULL, height=NULL, options=NULL, particlesLoaded=NULL, style=NULL, width=NULL) {
    
    props <- list(id=id, className=className, height=height, options=options, particlesLoaded=particlesLoaded, style=style, width=width)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashParticles',
        namespace = 'dash_particles',
        propNames = c('id', 'className', 'height', 'options', 'particlesLoaded', 'style', 'width'),
        package = 'dashParticles'
        )

    structure(component, class = c('dash_component', 'list'))
}
