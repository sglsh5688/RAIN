#!/usr/bin/env python3
"""The unchanged traced evaluator with exact second-stove instance bindings."""
import run_compose_traj_repair_evaluator_entry as base


def register_bindings():
    base.register_bindings()
    for instance in (1, 2):
        for key, suffix in ((f'flat_stove_{instance}', 'button'),
                            (f'flat_stove_{instance}_cook_region', 'burner')):
            name=f'flat_stove_{instance}_{suffix}'
            base.exact.benchmark_support.ACTION_OBJECTS[key]=dict(
                name=name,body_name=name,body_ids=[0],geom_ids=[],segmentable=True)


register_bindings()
if __name__=='__main__':base.exact.evaluator.main()
