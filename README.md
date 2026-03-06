# TurtleBot3 Burger Project (ROS2 Humble)

โปรเจคนี้ใช้ TurtleBot3 Burger บน ROS2 Humble เพื่อควบคุมหุ่นยนต์ด้วยจอยเกม โดยใช้แพ็กเกจ `joy` และ `teleop_twist_joy` พร้อมไฟล์ config ที่ปรับแต่งเอง (mapping ปุ่มจอย → ความเร็ว `/cmd_vel`) เพื่อให้รันตามได้ง่ายและไม่พังเมื่อย้ายตำแหน่งไฟล์

---

## Repository Structure
- `config/`
  - `my_teleop.yaml` : ไฟล์ mapping ปุ่มจอย → ความเร็วที่ส่งออก `/cmd_vel`
- `scripts/`
  - `setup.sh` : ตั้งค่า environment และรวมคำสั่งลัด (aliases) สำหรับรันงาน
- `docs/`
  - `block-diagram.png` : Block diagram ของระบบ
- `firmware/`
  - (ไฟล์ที่เกี่ยวกับ firmware ถ้ามี เช่น `.ino`)

---

## Requirements
- Ubuntu + **ROS2 Humble**
- TurtleBot3 Model: **burger**
- Packages: `joy`, `teleop_twist_joy`
- Joystick device เช่น `/dev/input/js0`, `/dev/input/js1`, `/dev/input/js2`

---

## Setup

เช็คว่าเครื่องเห็นจอย:
```bash
ls /dev/input/js\*
```

โหลด environment + aliases ของโปรเจค:
```bash
cd ~/Turtlebot3_Burger_Project
source scripts/setup.sh
```

ถ้าจอยของคุณไม่ใช่ js2 (เช่นเป็น js0) ให้ตั้ง JOY_DEV ก่อน แล้วค่อย source ใหม่:
```bash
export JOY_DEV=/dev/input/js0
source scripts/setup.sh
```

## Run

รัน joy_node:
```bash
run_joy
```

รัน teleop (เลือก 1 แบบ)

ใช้ config ของระบบ (PS3 ตัวอย่าง):
```bash
run_teleop
```

ใช้ config ของโปรเจค (แนะนำ):
```bash
go_racing
```

## Verify

ตรวจสอบว่าอ่านจอยได้:
```bash
ros2 topic echo /joy
```

ตรวจสอบว่ามีการส่งความเร็วออก (เวลาขยับจอยควรเห็นค่าเปลี่ยน):
```bash
ros2 topic echo /cmd_vel
```
## Troubleshooting

ถ้า error หาไฟล์ YAML ไม่เจอ: ตรวจสอบว่าไฟล์อยู่ที่ config/my_teleop.yaml และ scripts/setup.sh ชี้ path ถูกต้อง

ถ้า /joy ไม่ขึ้น: ตรวจสอบ device /dev/input/js* และลองเปลี่ยน JOY_DEV

ถ้า /cmd_vel ไม่ออก: ต้องรัน run_joy ก่อน แล้วค่อยรัน go_racing หรือ run_teleop

