from .nodes_rk_sampler import RungeKuttaSamplerImpl, ADAPTIVE_METHODS, METHODS

rk_samplers = []

_samplers = {}

for method_name in METHODS:
    is_adaptive = True if ADAPTIVE_METHODS.get(method_name, None) else False
    sampler = RungeKuttaSamplerImpl(
        method = method_name,
        step_size_controller = 'adaptive_pid' if is_adaptive else 'fixed_scheduled',
        log_absolute_tolerance = -3.5,
        log_relative_tolerance= -2.5,
        pcoeff = 0.0,
        icoeff = 1.0,
        dcoeff = 0.0,
        norm = "rms_norm",
        enable_dt_min = False,
        enable_dt_max = True,
        dt_min = -1.0,
        dt_max = 0.0,
        safety = 0.9,
        factor_min = 0.2,
        factor_max = 10.0,
        max_steps = 2 ** 31 - 1,
        min_sigma = 1.0e-5
        )
    _samplers[method_name] = sampler
    rk_samplers.append((METHODS[method_name].__name__, _samplers[method_name].__call__, [method_name], {}))