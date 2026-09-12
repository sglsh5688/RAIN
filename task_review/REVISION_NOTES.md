## 현재 지시문과 구획 표시 · 2026-09-12

로봇 팔 관점에 맞춘 두 Compose task의 현재 지시문은 다음과 같습니다.

**Compose_015 / CTR_103 — 버터 오른쪽 → 토마토소스 왼쪽**

> Pick the butter and place it in the right compartment of the bowl drainer, then pick the tomato sauce and place it in the left compartment of the bowl drainer

**Compose_018 / BDRMIN_002 — 수프 왼쪽 → 토마토소스 오른쪽**

> Pick the alphabet soup and place it in the left compartment of the bowl drainer, then pick the tomato sauce and place it in the right compartment of the bowl drainer

이번 후속 수정은 Compose_018의 현재 문구에 적용했습니다. [현재 지시문·원본 구획 비교](DRAINER_DIRECTIONS.png)는 문장에 쓰인 방향과 내부 goal ID를 따로 표시합니다. Compose_015의 내부 ID는 butter left_region → tomato sauce right_region, Compose_018의 내부 ID는 alphabet soup right_region → tomato sauce left_region으로 보존합니다. 카메라 화면의 좌우와 내부 구획 이름을 혼용하지 않도록 표시했습니다.

모든60개 현재 instruction의 마침표 제거, Adapt_009의 right compartment, Compose_019의 명시적 세 단계 순서는 유지합니다. 기존 변경을 합하면 최초 패키지 대비56개 instruction이 달라졌으며, 네 차례 전체 이력은 [문구 변경 기록](INSTRUCTION_REVISIONS.json)에 있습니다.

현재 설명·BDDL language·metadata·검수 이미지·Selected 페이지를 동기화했습니다. 물리적 목적지·초기 상태·goal ID·단계 순서·mask와 완료된 평가 결과는 그대로입니다. 영상과 행동별 source_task_description은 당시 평가 기록이므로 현재 전체 지시문과 구분해서 표시합니다.
