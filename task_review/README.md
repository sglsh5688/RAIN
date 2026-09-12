# LIBERO Analogy · Task 검수

[검수 페이지](index.html) · [Selected Tasks](../selected29/index.html) · [ID 대응표](ID_MAPPING.tsv)

새 ID를 사용하는 60개 task의 Task Description, 목표, 초기 scene, 행동 단계별 mask를 모았습니다. 카테고리별로 Decomposition_001–020, Adapt_001–020, Compose_001–020이며 이전 ID도 함께 표시합니다.

페이지에서 task와 단계를 선택한 뒤 Scene / Mask overlay / 이진 mask를 전환하세요. 별도 이동 목표가 있는 단계는 행동 대상과 목표 영역 mask를 나눠 볼 수 있습니다. 검수 상태와 메모는 브라우저에 저장되며, 내보내기를 누르면 전체60개 task의 검수 기록을 JSON으로 받을 수 있습니다. 이 기록은 자동으로 GitHub에 전송되지 않습니다.

모든 장면은 초기 상태0, seed7, 평가의10회 초기 안정화 control 직후입니다. 153개 행동 단계에 대해 RGB120장과 이진 mask444개를 저장했습니다. 13개 wrist mask는 이 초기 시야에서 보이지 않거나 투영할 수 없어 비어 있습니다. 다른 초기 배치나 행동 이후 장면은 포함하지 않습니다.

각 task의 `scenes/<Category>/<Task_ID>/TASK_REVIEW.png`에는 설명과 전체 단계 mask가 한 장으로 정리되어 있습니다. 카테고리 전체 보기: [Decomposition](overview/Decomposition.png), [Adapt](overview/Adapt.png), [Compose](overview/Compose.png).

영상은 완료된 RAIN 50episode 평가의 실제 성공59개·실패53개 대표 기록입니다. 이전 ID가 영상에 남아 있으며 대응표로 연결됩니다. 페이지의 성공률은 이50episode 평가 기준입니다. 과거 비교 이미지는 Selected Tasks 페이지에 있던 기존 자료입니다. 새로운 정책 추론이나 성공 영상의 추가 수동 인증은 수행하지 않았습니다.

공개 definition 파일은 task 의미와 판정 조건을 유지하며, 로컬 실행 경로는 `local-source:<filename>`로 표시했습니다. 현재 scene의 출처와 mask 정보는 task별 `scene.json`에 있습니다. [공개 자료 요약](REVIEW_SUMMARY.json), [영상 목록](VIDEO_INDEX.json), [한글 글꼴 라이선스](assets/NotoSans-LICENSE.txt)를 함께 제공합니다.

## 현재 지시문과 구획 표시 · 2026-09-12

로봇 팔 관점에 맞춘 두 Compose task의 현재 지시문은 다음과 같습니다.

**Compose_015 / CTR_103 — 버터 오른쪽 → 토마토소스 왼쪽**

> Pick the butter and place it in the right compartment of the bowl drainer, then pick the tomato sauce and place it in the left compartment of the bowl drainer

**Compose_018 / BDRMIN_002 — 수프 왼쪽 → 토마토소스 오른쪽**

> Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer

이번 후속 수정은 Compose_018의 현재 문구에 적용했습니다. [현재 지시문·원본 구획 비교](DRAINER_DIRECTIONS.png)는 문장에 쓰인 방향과 내부 goal ID를 따로 표시합니다. Compose_015의 내부 ID는 butter left_region → tomato sauce right_region, Compose_018의 내부 ID는 alphabet soup right_region → tomato sauce left_region으로 보존합니다. 카메라 화면의 좌우와 내부 구획 이름을 혼용하지 않도록 표시했습니다.

모든60개 현재 instruction의 마침표 제거, Adapt_009의 right compartment, Compose_019의 명시적 세 단계 순서는 유지합니다. 기존 변경을 합하면 최초 패키지 대비56개 instruction이 달라졌으며, 네 차례 전체 이력은 [문구 변경 기록](INSTRUCTION_REVISIONS.json)에 있습니다.

현재 설명·BDDL language·metadata·검수 이미지·Selected 페이지를 동기화했습니다. 물리적 목적지·초기 상태·goal ID·단계 순서·mask와 완료된 평가 결과는 그대로입니다. 영상과 행동별 source_task_description은 당시 평가 기록이므로 현재 전체 지시문과 구분해서 표시합니다.
