# Adapt_009

Legacy ID: `ANLGX_178`

## Task Description

Put the yellow and white mug in the right compartment of the caddy

## 목표

- in(white_yellow_mug_1, desk_caddy_1_left_contain_region)

## 금지 목표

없음

## Scene / mask

초기 상태 index 0, seed 7. 모든 단계의 mask는 같은 초기 scene에서 표시합니다. 이후 로봇 행동의 진행 장면이 아닙니다.

[단계별 mask 검수 화면](../../../index.html#Adapt_009)

[Scene 기록 및 이미지 경로](scene.json)

## Compartment 방향

현재 지시문의 right compartment는 로봇 베이스 기준 오른쪽 칸입니다. Caddy가 180° 회전되어 있어 원본 구획 ID는 left_contain_region입니다. 기존 평가 mask는 caddy 전체를 표시하며, 오른쪽 칸만 분리한 mask는 아닙니다.

[로봇 기준과 원본 구획 방향 비교](../../../COMPARTMENT_FRAMES.png)
