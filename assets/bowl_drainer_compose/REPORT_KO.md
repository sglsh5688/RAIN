# Bowl Drainer — 완료된 위치 교환 평가

`BDRSWAP_001`: 원본 5episode 중 native In 5/5 (100%).

Pick the alphabet soup and place it in the right compartment of the bowl drainer.

기준 BDRSIDE_002의 같은 다섯 초기 상태에서 alphabet soup와 salad dressing의 XY 위치만 서로 교환했습니다. 각 물체의 Z·quaternion, 나머지 네 물체, 로봇, drainer, goal·mask·평가 규칙은 보존했습니다.

비교 PNG 세 패널은 원본 LIBERO_OBJECT_01 / 기준 BDRSIDE_002 / 새 BDRSWAP_001입니다. 원본과 새 task 모두 상호작용 mask를 표시합니다. 새 task는 로봇 기준 오른쪽 native 칸만 destination mask로 사용하며 양쪽 union mask가 아닙니다.

**Native 성공은 release·안착 성공이 아닙니다.** 지정 칸에 물체 중심이 들어오면 종료될 수 있습니다. 실제 종료 시 drainer 접촉 0/5이며, 손을 놓고 바닥에 지지된 성공률은 측정하지 않았습니다. 다른 Composition의 strict 결과와 합산하지 않습니다.

원본 5개 영상 모두 포함합니다. 실패가 없으므로 별도 실패 영상도 없으며, 실패 영상 확보를 위해 추가 rollout을 만들지 않았습니다. 진행 중인 두 물체 Composition 평가와 별개의 완료된 atomic swap 결과입니다.

| Episode | Native success | 종료 drainer 접촉 | 종료 floor 접촉 | 영상 |
|---|---|---|---|---|
| 0 | True | False | False | [원본 MP4](videos/BDRSWAP_001_ep000_ok.mp4) |
| 1 | True | False | False | [원본 MP4](videos/BDRSWAP_001_ep001_ok.mp4) |
| 2 | True | False | False | [원본 MP4](videos/BDRSWAP_001_ep002_ok.mp4) |
| 3 | True | False | False | [원본 MP4](videos/BDRSWAP_001_ep003_ok.mp4) |
| 4 | True | False | False | [원본 MP4](videos/BDRSWAP_001_ep004_ok.mp4) |

GPU 6 · 5episode · 기존 RAIN multi-scale/mask-augmentation checkpoint · seed 7 · 원래 native In 평가.

- Action checkpoint SHA256: `7232043efb5b6d563def9fa378cd6f16b8e4623e103327605a5203714807252f`
- Progress checkpoint SHA256: `e35566c8f366b49c79fd4e029b42ccde56438bd270f895fd286482febb605eae`

비교 썸네일 하나만 먼저 내려받고, 원본 PNG는 확대할 때, MP4는 재생할 때만 로드합니다. 영상 preload는 none이며 MP4 faststart·전체 decode를 확인했습니다. 서비스 자체의 요청 제한을 완전히 보장할 수는 없습니다.
