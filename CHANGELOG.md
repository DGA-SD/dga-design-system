# Changelog

รูปแบบตาม Keep a Changelog และ Semantic Versioning

## [Unreleased]

### เปลี่ยน

- ฝ่าย SD ยืนยัน (2026-10-09) ให้ใช้ค่าใน design system นี้เป็นหลักทั้งฟอนต์ (Prompt, Sarabun สำหรับบทความ) ค่าสี และโลโก้ ปรับ SOURCE.md และ README.md ให้ตรง

## [1.0.0] - 2026-10-09

เวอร์ชันแรก นำเข้าจาก claude.ai Design System artifact ที่สกัดจาก dga.or.th (ดู SOURCE.md)

### เพิ่ม

- brand book `design-system/README.md`: เสียงของแบรนด์ กติกาสี ฟอนต์ ระยะ รูปภาพ ไอคอน โลโก้
- token 24 สี x 2 ธีม (light, dark), 18 type style ใน 3 กลุ่ม (Web, Article, Slides), 10 ระยะ, 5 มุมโค้ง, 4 เงา
- component 13 ตัว: ArticleBody, Badge, Button, Callout, Footer, NavBar, NewsCard, SectionHeader, ServiceTile, SlideContent, SlideSection, SlideTitle, StatBlock พร้อม Cover
- `tokens.css` และ `components/bundle.css` ใช้งานได้ทันที
- โลโก้ DGA `assets/Logos/dga-logo.webp`
- export W3C DTCG ใน `tokens/dtcg/` (base, light, dark)
- หน้า gallery `design-system/index.html`
- `AGENTS.md` สำหรับ AI coding agent
- สคริปต์ generate ใน `tools/`

### ยังไม่ยืนยัน (ณ วันออก 1.0.0)

- ฟอนต์หลัก (Prompt หรือ Anuphan) และค่าสีส้ม/กรมท่าที่ต่างกันระหว่าง dga.or.th กับ standard.dga.or.th ดู SOURCE.md
