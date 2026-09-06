#!/usr/bin/env python3
"""Evaluate three authorized native-Goal rack object substitutions, five trials each."""
import argparse
import csv
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

import run_extra75_tc9_eval as common

ROOT = Path(__file__).resolve().parent
BENCHMARK = ROOT / 'LiberoAdaptGoalRackObjects20260906'
ENTRY = ROOT / 'run_wine_rack_objects_evaluator_entry.py'
SITE = 'wine_rack_1_adapt_top_region'
SPECS = {
    'GRACK_001': ('alphabet_soup_1', 'Put the alphabet soup on the rack.', 6),
    'GRACK_002': ('ketchup_1', 'Put the ketchup on the rack.', 7),
    'GRACK_003': ('new_salad_dressing_1', 'Put the salad dressing on the rack.', 6),
}
METRIC = 'Actual upper-deck footprint and positive physical upper-deck support, released without gripper contact for five consecutive controls; original wine-specific native On is auxiliary'
_original_command = common.build_command


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def command(args, job, gpu):
    cmd = _original_command(args, job, gpu)
    cmd[cmd.index('--max-fail-videos') + 1] = '5'
    return cmd


common.EVALUATOR = ENTRY
common.build_command = command


def fingerprint():
    filenames = ('run_goal_rack_objects_5ep.py', 'run_wine_rack_objects_evaluator_entry.py',
        'wine_rack_object_support.py', 'build_goal_rack_objects.py', 'run_extra75_tc9_eval.py',
        'run_diverse_adapt_evaluator_entry.py', 'run_analogy_evaluator_entry.py',
        'cream_cheese_bowl_layout.py', 'novel_scene_common.py', 'novel_feedback_object_bindings.py',
        'novel_feedback_fixture_geometry.py',
        'diverse_adapt_mask_geometry.py', 'build_libero_analogy.py', 'build_libero_analogy_expanded.py')
    runtime = [ROOT / name for name in filenames]
    runtime += sorted((common.RAIN_ROOT / 'final_libero_ex_eval/impl').glob('*.py'))
    libero_env = Path('/path/to/libero/envs')
    runtime += [libero_env / name for name in ('objects/site_object.py',
        'object_states/base_object_states.py', 'predicates/base_predicates.py')]
    benchmark = [BENCHMARK / name for name in ('TASK_INDEX.tsv', 'registry.yaml', 'action_plan_registry.yaml', 'BUILD_VALIDATION.json',
        'GEOMETRY_SPEC.json', 'GEOMETRY_WITNESS_VALIDATION.json',
        'REGION_CORRECTION_VALIDATION.json', 'SOURCE_PRESERVATION.json')]
    for name in ('tasks', 'benchmark_support', 'comparison_png'):
        benchmark += [p for p in (BENCHMARK / name).rglob('*') if p.is_file()]
    asset_root = Path('/path/to/libero_assets')
    assets = []
    for rel in ('turbosquid_objects/wine_rack', 'stable_hope_objects/alphabet_soup',
                'stable_hope_objects/ketchup', 'stable_hope_objects/new_salad_dressing'):
        folder = asset_root / rel
        assert folder.is_dir()
        assets += [p for p in folder.rglob('*') if p.is_file()]
    result = dict(runtime={str(p): sha(p) for p in runtime},
        benchmark={str(p.relative_to(BENCHMARK)): sha(p) for p in benchmark},
        assets={str(p): sha(p) for p in assets},
        action_checkpoint=common.checkpoint_metadata(common.DEFAULT_ACTION),
        progress_checkpoint=common.checkpoint_metadata(common.DEFAULT_PROGRESS))
    previous = json.loads((ROOT / 'LiberoAdaptWoodenShelf20260906/evaluation_5ep/WSHELF_001/raw_results/run_config.json').read_text())['frozen_artifacts']
    for key in ('action_checkpoint', 'progress_checkpoint'):
        assert result[key]['sha256'] == previous[key]['sha256'], 'Checkpoint must remain unchanged'
    return result


def validate(task_id):
    sys.path.insert(0, str(common.RAIN_ROOT))
    importlib.import_module(ENTRY.stem)
    import torch
    from final_libero_ex_eval.impl.benchmark_support import LiberoEXBenchmark
    from final_libero_ex_eval.impl.conditions import build_libero_ex_conditions
    from cream_cheese_bowl_layout import state_hash
    from libero.libero.envs.bddl_utils import robosuite_parse_problem
    rows = common.read_tsv(BENCHMARK / 'TASK_INDEX.tsv')
    assert len(rows) == 3 and {r['task_id'] for r in rows} == set(SPECS)
    row = next(r for r in rows if r['task_id'] == task_id)
    bench = LiberoEXBenchmark(benchmark_root=str(BENCHMARK))
    assert bench.get_num_tasks() == 3
    index = next(i for i in range(3) if bench.get_task(i).task_id == task_id)
    obj, language, _ = SPECS[task_id]
    assert bench.get_task(index).language == language
    parsed = robosuite_parse_problem(bench.get_task_bddl_file_path(index))
    assert parsed['goal_state'] == [['on', obj, SITE]]
    assert {o for group in parsed['objects'].values() for o in group} == {obj, 'cream_cheese_1', 'akita_black_bowl_1', 'plate_1'}
    meta, rules = bench.get_task_meta(index), bench.get_task_eval_rules(index)
    assert meta['evaluation_authorized'] and meta['policy_evaluation_authorized']
    assert meta['single_semantic_goal'] and rules['custom_eval_needed']
    assert rules['native_goal_required'] is False and rules['annotated_goal_required'] is True
    assert rules['legacy_native_on_auxiliary_only'] is True
    assert rules['final_tc_gate'] is False and rules['support_hold_control_steps'] == 5
    episode, conditions = build_libero_ex_conditions(meta, bench.get_task_action_plan(index), 224)
    assert [(c.action_type,c.object_id) for c in conditions] == [('grasp',obj),('release',SITE)]
    assert episode['objects'][obj]['name'] == obj + '_main'
    assert episode['objects'][SITE]['name'] == 'wine_rack_1_main' and episode['objects'][SITE]['segmentable']
    states = torch.load(bench.get_task_init_states_path(index), weights_only=False, map_location='cpu')
    hashes = [state_hash(s) for s in states]
    replay = json.loads((BENCHMARK / row['bundle'] / 'FIXTURE_REPLAY.json').read_text())['rows']
    assert len(set(hashes)) == len(hashes) == 5
    assert hashes == [r['state_sha256'] for r in replay]
    assert all(r.get('settled_body_positions') and r.get('fixture_model_poses') for r in replay)
    witnesses = json.loads((BENCHMARK / 'GEOMETRY_WITNESS_VALIDATION.json').read_text())
    assert witnesses['all_three_positive_witnesses_passed'], 'All three physical goal witnesses must pass before policy evaluation'
    return row, index, hashes


def audit(args, job, row, hashes, config, execution):
    import imageio_ffmpeg
    from wine_rack_object_support import strict_instant
    raw = common.task_dir(args, job)
    episodes = common.result_rows(raw / 'results.json', job, 5)
    assert episodes is not None and fingerprint() == config['frozen_artifacts']
    obj, language, _ = SPECS[job.task_id]
    exposed = BENCHMARK / 'evaluation_5ep/videos' / job.task_id
    exposed.mkdir(parents=True, exist_ok=True)
    media = []
    for episode in episodes:
        idx, meta = episode['episode_idx'], episode['meta']
        placement = meta['rack_object_placement']
        records = placement['records']
        assert meta['initial_goal_satisfied'] is False and meta['initial_state_sha256'] == hashes[idx]
        assert meta['init_state_index'] == idx and meta['initial_body_position_max_abs_diff'] <= 1e-8
        assert meta['fixture_replay_calls'] == 2
        assert [r['control_step'] for r in records] == list(range(meta['total_steps'] + 1))
        hold = maximum = 0
        for fact in records:
            instant = strict_instant(fact)
            hold = hold + 1 if instant else 0
            maximum = max(maximum, hold)
            assert instant == fact['strict_instant'] and hold == fact['consecutive_supported_steps']
        assert bool(episode['success']) == (hold >= 5) == placement['strict_released_supported_success']
        assert maximum == placement['maximum_consecutive_supported_steps']
        masks = meta['rack_object_active_mask_audit']
        assert masks and meta['rack_object_inference_payload_audit']
        for entry in masks:
            assert entry['mask_source'] in ('sim_seg', 'sim_missing')
            assert entry['object_id'] == (obj if entry['action_type'] == 'grasp' else SITE)
        outcome = 'ok' if episode['success'] else 'fail'
        video = raw / 'videos' / f'{job.task_id}_ep{idx:03d}_{outcome}.mp4'
        assert video.is_file()
        decoded = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v','error','-xerror','-i',str(video),'-f','null','-'], capture_output=True,text=True)
        assert decoded.returncode == 0, decoded.stderr
        target = exposed / video.name
        if not target.exists():
            try:
                os.link(video,target)
            except OSError:
                shutil.copy2(video,target)
        assert sha(target) == sha(video)
        media.append(dict(task_id=job.task_id,episode_idx=idx,success=bool(episode['success']),
            video=str(target),sha256=sha(video),raw_video=str(video),total_steps=meta['total_steps'],
            maximum_supported_hold=maximum,adapt_on_final=bool(records[-1]['annotated_on']),
            native_on_final=bool(records[-1]['native_on']),
            native_on_ever=any(r['native_on'] for r in records)))
    assert len(list((raw / 'videos').glob('*.mp4'))) == 5
    shutil.copy2(BENCHMARK / row['comparison_png'], exposed / 'comparison.png')
    successes = sum(r['success'] for r in episodes)
    summary = dict(task_id=job.task_id,instruction=language,successes=successes,episodes=5,
        success_rate_percent=20*successes,gpu=args.gpu,actual_episode_seeds=config['actual_episode_seeds'],
        native_on_final_count=sum(r['native_on_final'] for r in media),
        native_on_ever_count=sum(r['native_on_ever'] for r in media),
        video_directory=str(exposed),result_path=str(raw/'results.json'),metric=METRIC)
    common.atomic_json(args.output/'FINAL_EVALUATION_AUDIT.json',dict(passed=True,summary=summary,media=media,
        all_original_videos_decode=True,every_control_strict_hold_replayed=True,
        frozen_sources_unchanged=True,raw_results_sha256=sha(raw/'results.json'),execution=execution))
    common.atomic_json(args.output/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False),flush=True)


def report():
    audits = [json.loads((BENCHMARK/'evaluation_5ep'/task/'raw_results/FINAL_EVALUATION_AUDIT.json').read_text()) for task in SPECS]
    assert all(r['passed'] for r in audits)
    summaries = [r['summary'] for r in audits]
    total = sum(r['successes'] for r in summaries)
    lines = ['# Goal wine-rack object substitution — 5 episodes each','',
        '| Task ID | Task instruction | Success | SR | GPU |','|---|---|---:|---:|---:|']
    lines += [f"| {s['task_id']} | {s['instruction']} | {s['successes']}/5 | {s['success_rate_percent']}% | {s['gpu']} |" for s in summaries]
    lines += ['',f'전체: **{total}/15 ({100*total/15:.1f}%)**. 성공 episode가 있는 task: **{sum(s["successes"]>0 for s in summaries)}/3**.','',
        '원본: LIBERO_GOAL_10 — Put the wine bottle on the rack. 원본 wine의 XY에서 target만 교체했고 나머지 원본 배치와 rack 방향은 유지했습니다.',
        '각 새 물체는 원래 크기와 고유 orientation을 유지하고 바닥 높이만 실제 충돌 형상에 맞게 설정했습니다.',
        '기존 RAIN multi-scale + mask-augmentation action/progress checkpoint; 각 task 실제 seed 7–11, max steps 520, replan 8, inference steps 4, feasibility 0.7, consecutive-stop 2.',
        '원본 wine-rack placement와 동일하게 rack 전체의 실시간 GT body mask를 사용했습니다. 실제 윗판 영역 및 양의 지지력, gripper 접촉 해제 상태를 연속 5 control step 요구했습니다.',
        '정책 평가 전에 물리 검증에서 원본 wine용 좁은 top_region이 정상 지지된 alphabet soup를 거절하는 문제가 확인됐습니다. 장면이나 물리 asset은 그대로 두고 새 Adapt goal site를 실제 윗판 크기/좌표계에 맞게 정의했습니다. 원본 wine용 native On 코드는 수정하지 않았으며 별도 보조 지표입니다.',
        '성공률은 위 Adapt physical 조건 기준입니다. 원본 wine native On final/ever는 성공률과 구분해 별도로 기록했습니다. 5episode는 소규모 탐색 결과입니다.',
        '성공/실패 원본 영상 총 15개를 모두 저장했습니다. 성공 여부에 따른 재시도나 자동 task 수정은 없습니다.','',
        '| Task ID | Native On final | Native On ever |','|---|---:|---:|']
    lines += [f"| {s['task_id']} | {s['native_on_final_count']}/5 | {s['native_on_ever_count']}/5 |" for s in summaries]
    for a in audits:
        s = a['summary']
        lines += ['',f"## {s['task_id']}",'',f"[영상 폴더]({s['video_directory']})",'',
            '| Episode | Result | Video |','|---|---|---|']
        lines += [f"| {m['episode_idx']:03d} | {'Success' if m['success'] else 'Failure'} | [{Path(m['video']).name}]({m['video']}) |" for m in a['media']]
    (BENCHMARK/'EVALUATION_5EP_RESULTS.md').write_text('\n'.join(lines)+'\n')
    common.atomic_json(BENCHMARK/'evaluation_5ep/SUMMARY.json',dict(task_summaries=summaries,total_successes=total,total_episodes=15,overall_SR_percent=100*total/15))
    with (BENCHMARK/'evaluation_5ep/SUMMARY.tsv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(summaries[0]),delimiter='\t')
        writer.writeheader();writer.writerows(summaries)
    print(json.dumps(summaries,ensure_ascii=False,indent=2),flush=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task',choices=list(SPECS))
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--audit-only',action='store_true')
    parser.add_argument('--report',action='store_true')
    opts=parser.parse_args()
    if opts.report:
        report();return
    if not opts.task:
        parser.error('--task is required except with --report')
    row,index,hashes=validate(opts.task)
    obj,language,gpu=SPECS[opts.task]
    output=BENCHMARK/'evaluation_5ep'/opts.task/'raw_results'
    args=argparse.Namespace(**vars(opts),gpu=gpu,python=common.DEFAULT_PYTHON,
        action_checkpoint=common.DEFAULT_ACTION,progress_checkpoint=common.DEFAULT_PROGRESS,
        episodes_json=common.DEFAULT_EPISODES,benchmark=BENCHMARK,output=output,
        episodes=5,max_success_videos=5,seed=7-100*index,max_steps=520,replan_steps=8,
        num_inference_steps=4,feas_threshold=.7,consecutive_stop=2,cpu_threads=1,
        startup_stagger=0,stall_timeout_minutes=35,max_retries=0)
    job=common.Job(index,opts.task,language,'Adapt','all1',str(BENCHMARK))
    cmd=command(args,job,gpu)
    print(json.dumps(dict(preflight='PASS',task=opts.task,gpu=gpu,actual_episode_seeds=list(range(7,12)),command=cmd)),flush=True)
    if not opts.run and not opts.audit_only:
        return
    output.mkdir(parents=True,exist_ok=True)
    config_path=output/'run_config.json'
    if opts.audit_only:
        audit(args,job,row,hashes,json.loads(config_path.read_text()),dict(audit_only=True));return
    status=common.gpu_snapshot([gpu],False)[0]
    assert status['memory_total_mib']-status['memory_used_mib'] >= 16384,'Insufficient GPU memory; no unrelated jobs will be stopped'
    config=dict(created_at_utc=common.utc_now(),task_id=opts.task,episodes_per_task=5,
        physical_gpus=[gpu],seed=args.seed,task_index=index,actual_episode_seeds=list(range(7,12)),
        init_state_sha256=hashes,max_steps=520,replan_steps=8,num_inference_steps=4,
        feas_threshold=.7,consecutive_stop=2,max_success_videos=5,max_fail_videos=5,
        strict_support_hold_control_steps=5,primary_metric=METRIC,final_tc_gate=False,
        command=cmd,frozen_artifacts=fingerprint())
    if config_path.exists():
        previous=json.loads(config_path.read_text())
        assert all(previous.get(k)==v for k,v in config.items() if k!='created_at_utc'),'Frozen existing run differs'
        config=previous
    else:
        common.atomic_json(config_path,config)
    cache=common.prepare_text_cache(args,[job],{opts.task:language})
    execution=common.run_job(args,job,gpu,cache)
    audit(args,job,row,hashes,config,execution)


if __name__=='__main__':
    signal.signal(signal.SIGTERM,common.stop_all)
    signal.signal(signal.SIGINT,common.stop_all)
    main()
