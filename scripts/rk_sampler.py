from modules import scripts
from modules import sd_samplers, sd_samplers_common, script_callbacks
from modules.sd_samplers_common import SamplerData
from modules.sd_samplers_kdiffusion import KDiffusionSampler

from nodes.nodes_rk_sampler import RungeKuttaSamplerImpl, ADAPTIVE_METHODS, METHODS

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


incant_samplers_data_k_diffusion = [
    sd_samplers_common.SamplerData(label, lambda model, funcname = funcname: KDiffusionSampler(funcname, model), aliases, options)
    for label, funcname, aliases, options in rk_samplers 
]


def add_samplers(*args, **kwargs):
    sampler_list = incant_samplers_data_k_diffusion
    for sampler in sampler_list:
        exists = any([sampler.name == x.name for x in sd_samplers.all_samplers])
        if exists:
            continue
        sd_samplers.all_samplers.append(sampler)
        sd_samplers.all_samplers_map.update({sampler.name: sampler})
    sd_samplers.set_samplers()


script_callbacks.on_before_ui(add_samplers)


class RKSampler(scripts.Script):
    def __init__(self):
        self.infotext_fields: list = []
        self.paste_field_names: list = []

    def title(self) -> str:
        return "RK Sampler"

    def ui(self, is_img2img) -> list:
        return []

    def get_infotext_fields(self) -> list:
        return self.infotext_fields

    def get_paste_field_names(self) -> list:
        return self.paste_field_names

    def get_xyz_axis_options(self) -> dict:
        raise NotImplementedError

    def __init__(self):
        self.infotext_fields: list = []
        self.paste_field_names: list = []

    # Decide to show menu in txt2img or img2img
    def show(self, is_img2img):
            return scripts.AlwaysVisible
