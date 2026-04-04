
module DashParticles
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.2"

include("jl/'dp'_dashparticles.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "dash_particles",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "async-DashParticles.js",
    external_url = "https://unpkg.com/dash_particles@0.0.2/dash_particles/async-DashParticles.js",
    dynamic = nothing,
    async = :true,
    type = :js
),
DashBase.Resource(
    relative_package_path = "async-DashParticles.js.map",
    external_url = "https://unpkg.com/dash_particles@0.0.2/dash_particles/async-DashParticles.js.map",
    dynamic = true,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_particles.min.js",
    external_url = nothing,
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "dash_particles.min.js.map",
    external_url = nothing,
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
