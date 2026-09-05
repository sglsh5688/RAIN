# Adapt Object 평가 결과

원본 `LIBERO_OBJECT_01–10` 각각에서 scene, object 구성·위치, basket, init states를 그대로 두고, 원본 goal object를 제외한 나머지 5개 object를 한 번씩 새 타깃으로 지정했다.

- Task: **50개** (`10 scenes × 5 alternate objects`)
- 평가: **task당 5 episode, 총 250 episode**
- 성공 task: **7/50개**
- 성공 episode: **15/250 (6.0%)**
- 실행 장치: **physical GPU 6**
- 평가 mask: exact simulator GT with audited fallback; unexpected/online mask point 0개

## 성공한 task

| Task | 원본 scene | 원본 target → 새 target | 성공 | 성공 episode | 상태 | Instruction |
|---|---|---|---:|---|---|---|
| `OGDTSL_006` | `LIBERO_OBJECT_04` | bbq sauce → chocolate pudding | 2/5 (40.0%) | 1,4 | 후보 | Pick the chocolate pudding and place it in the basket |
| `OGDTSL_011` | `LIBERO_OBJECT_07` | butter → tomato sauce | 4/5 (80.0%) | 0,2,3,4 | Adapt selected | Pick the tomato sauce and place it in the basket |
| `OGDTSL_016` | `LIBERO_OBJECT_09` | chocolate pudding → orange juice | 1/5 (20.0%) | 1 | 후보 | Pick the orange juice and place it in the basket |
| `OGDTSL_021` | `LIBERO_OBJECT_02` | cream cheese → alphabet soup | 2/5 (40.0%) | 0,2 | 후보 | Pick the alphabet soup and place it in the basket |
| `OGDTSL_031` | `LIBERO_OBJECT_08` | milk → cream cheese | 3/5 (60.0%) | 1,2,3 | 후보 | Pick the cream cheese and place it in the basket |
| `OGDTSL_036` | `LIBERO_OBJECT_10` | orange juice → butter | 1/5 (20.0%) | 1 | 후보 | Pick the butter and place it in the basket |
| `OGDTSL_046` | `LIBERO_OBJECT_06` | tomato sauce → milk | 2/5 (40.0%) | 1,2 | Adapt selected | Pick the milk and place it in the basket |

## 위치별 결과

| 새 target의 원본 위치 근거 | Tasks | 성공 episode | SR |
|---|---:|---:|---:|
| 다른 원본 task에서 target-interaction 위치로 관측됨 | 10 | 15/50 | 30.0% |
| 현재 원본 scene에서 distractor-only 위치 | 40 | 0/200 | 0.0% |

15번의 성공은 전부 첫 번째 위치군에서 나왔다. 즉 object 종류만 바꾸는 것뿐 아니라, 새 object가 학습 중 target으로 상호작용했던 위치에 놓여 있는지가 이 평가에서 큰 차이를 보였다.

## 무결성 확인

- 50개 task 및 250개 `(task_id, episode_idx)` 키의 누락·중복 없음
- 원본마다 여섯 scene object 중 원본 target을 제외한 다섯 object가 정확히 한 번씩 포함됨
- 후보 BDDL의 region geometry와 모든 object init mapping이 원본과 동일함
- 후보 `.pruned_init` bytes가 해당 원본 LIBERO-Object init states와 동일함
- 성공 영상 15/15개 outcome 일치 및 전체 frame decode 확인
- 원 평가의 run config, aggregate, inventory, registry SHA-256을 `AUDIT.json`에 기록함
