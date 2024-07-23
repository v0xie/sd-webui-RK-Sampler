import launch

if not launch.is_installed('torchode'):
    launch.run_pip("install torchode", "sd-webui-RK-Sampler: installing torchode")