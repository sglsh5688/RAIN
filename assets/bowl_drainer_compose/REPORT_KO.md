# Bowl Drainer — Two-Object Composition / Swap 결과

- Composition: 40 task × 5episode, strict 성공 5/200 (2.5%), 성공 task 4/40.
- 같은 strict rollout의 native final AND 보조 관측: 5/200. Native ordered final 보조: 5/200.
- 300개 후보 중 40개만 policy 평가. 나머지 260개는 미평가입니다.
- 이전 atomic XY swap: native 5/5 (100%). 종료 drainer 접촉 0/5이며 release/support SR은 미측정입니다. Composition strict 결과와 합산하지 않습니다.

## 판정·마스크

A를 로봇 기준 왼쪽 칸에 먼저, B를 오른쪽 칸에 나중에 놓습니다. Drainer는 한 episode 내내 고정입니다. Strict milestone은 selected native In + gripper 비접촉 + 정확한 native 바닥 geom의 양의 접촉력이 5 control step 연속 유지되는 조건입니다. 종료 시 두 물체가 모두 조건을 유지해야 합니다. 속도 기반 완전 정착 인증이나 물체 전체 3D containment 판정은 아닙니다.

Native 값은 같은 strict rollout에서 관측한 보조 지표입니다. Native first-entry로 종료한 별도 평가와 직접 동일시하지 않습니다. 수동 geometry witness, 초기 상태 검증, 기술적으로 무효인 이전 run은 policy SR에 포함하지 않았습니다.

비교 PNG의 두 stage 모두 같은 초기 장면의 마스크 미리보기입니다. Step 2는 step 1 수행 뒤의 rollout이 아닙니다. 원본 LIBERO mask와 새 task의 정확한 단계별 물체/칸 mask를 비교합니다. 현재 action과 이전 단계 TC 입력 모두 정확한 native region mask를 사용한 수정 run만 포함합니다.

## Task별 결과

| Task ID | Original | Instruction | Strict | Native final AND (보조) |
|---|---|---|---|---|
| BDRCOMP_001 | LIBERO_OBJECT_01 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_002 | LIBERO_OBJECT_01 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_003 | LIBERO_OBJECT_02 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_004 | LIBERO_OBJECT_02 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 1/5 (20%) | 1/5 |
| BDRCOMP_005 | LIBERO_OBJECT_03 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_006 | LIBERO_OBJECT_03 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_007 | LIBERO_OBJECT_04 | Pick the chocolate pudding and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 1/5 (20%) | 1/5 |
| BDRCOMP_008 | LIBERO_OBJECT_04 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_009 | LIBERO_OBJECT_05 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_010 | LIBERO_OBJECT_05 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_011 | LIBERO_OBJECT_06 | Pick the tomato sauce and place it in the left compartment of the bowl drainer, then pick the butter and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_012 | LIBERO_OBJECT_06 | Pick the butter and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_013 | LIBERO_OBJECT_07 | Pick the butter and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_014 | LIBERO_OBJECT_07 | Pick the tomato sauce and place it in the left compartment of the bowl drainer, then pick the butter and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_015 | LIBERO_OBJECT_08 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_016 | LIBERO_OBJECT_08 | Pick the tomato sauce and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_017 | LIBERO_OBJECT_09 | Pick the chocolate pudding and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_018 | LIBERO_OBJECT_09 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_019 | LIBERO_OBJECT_10 | Pick the butter and place it in the left compartment of the bowl drainer, then pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_020 | LIBERO_OBJECT_10 | Pick the chocolate pudding and place it in the left compartment of the bowl drainer, then pick the butter and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_021 | LIBERO_OBJECT_01 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the salad dressing and place it in the right compartment of the bowl drainer. | 2/5 (40%) | 2/5 |
| BDRCOMP_022 | LIBERO_OBJECT_01 | Pick the salad dressing and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_023 | LIBERO_OBJECT_02 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the milk and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_024 | LIBERO_OBJECT_02 | Pick the milk and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_025 | LIBERO_OBJECT_03 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the salad dressing and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_026 | LIBERO_OBJECT_03 | Pick the salad dressing and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_027 | LIBERO_OBJECT_04 | Pick the chocolate pudding and place it in the left compartment of the bowl drainer, then pick the bbq sauce and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_028 | LIBERO_OBJECT_04 | Pick the bbq sauce and place it in the left compartment of the bowl drainer, then pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_029 | LIBERO_OBJECT_05 | Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the ketchup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_030 | LIBERO_OBJECT_05 | Pick the ketchup and place it in the left compartment of the bowl drainer, then pick the alphabet soup and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_031 | LIBERO_OBJECT_06 | Pick the tomato sauce and place it in the left compartment of the bowl drainer, then pick the milk and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_032 | LIBERO_OBJECT_06 | Pick the milk and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_033 | LIBERO_OBJECT_07 | Pick the butter and place it in the left compartment of the bowl drainer, then pick the orange juice and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_034 | LIBERO_OBJECT_07 | Pick the orange juice and place it in the left compartment of the bowl drainer, then pick the butter and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_035 | LIBERO_OBJECT_08 | Pick the cream cheese and place it in the left compartment of the bowl drainer, then pick the milk and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_036 | LIBERO_OBJECT_08 | Pick the milk and place it in the left compartment of the bowl drainer, then pick the cream cheese and place it in the right compartment of the bowl drainer. | 1/5 (20%) | 1/5 |
| BDRCOMP_037 | LIBERO_OBJECT_09 | Pick the chocolate pudding and place it in the left compartment of the bowl drainer, then pick the orange juice and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_038 | LIBERO_OBJECT_09 | Pick the orange juice and place it in the left compartment of the bowl drainer, then pick the chocolate pudding and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_039 | LIBERO_OBJECT_10 | Pick the butter and place it in the left compartment of the bowl drainer, then pick the orange juice and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |
| BDRCOMP_040 | LIBERO_OBJECT_10 | Pick the orange juice and place it in the left compartment of the bowl drainer, then pick the butter and place it in the right compartment of the bowl drainer. | 0/5 (0%) | 0/5 |

## 원본 영상과 provenance

40개 task마다 원본 5episode의 성공/실패 영상 전부와 swap 원본 5개 영상을 보존했습니다. 추가 rollout을 만들거나 성공 영상을 재연하지 않았습니다. MP4는 무손실 container faststart 변환만 허용하고 전체 decode 검증합니다. 영상별 원본/패키지 SHA256은 MEDIA_MANIFEST.tsv에 있습니다.

비교 썸네일은 하나의 WebP sprite이고 PNG와 영상은 사용자 선택 시에만 로드합니다. 기존 offline ZIP은 교체 전에 별도 backup 폴더에 보존됩니다.

## 구현 버전과 추가 mask 검증 범위

이 결과는 **기존 V2 완료 86episode + 남은 원본 114episode를 V3로 이어서 평가한 결과**입니다. V2 86개 JSONL 원본 행·canonical 기록·영상은 SHA256 ledger로 검증해 그대로 유지했고, 재실행하거나 판정을 바꾸지 않았습니다. 원래 40개 registry index, episode 0–4, 초기 상태, seed, 체크포인트, text feature의 동일성을 확인했습니다.

V3는 현재 agentview grasp mask가 없다고 나온 분기에 한해 실제 raw segmentation 렌더링과 정확한 기존 geom binding을 확인하여 해당 객체가 현재 화면에 0 pixel인 경우를 구분합니다. 정상 mask 출력, 이전-TC/wrist helper, action·TC 전환·물리적 성공 판정은 바꾸지 않았습니다.

**기존 V2 86개에서 wrist 또는 previous-TC mask가 None이었던 물리적 원인을 소급 검증하지 않았습니다.** 200개 전체가 동일한 V3 availability 진단을 받았다고 표시하지 않습니다. 추가 진단은 새 114개에만 적용됩니다. Task/episode TSV·JSON에서 원본 V2와 새 V3를 구분할 수 있습니다.
