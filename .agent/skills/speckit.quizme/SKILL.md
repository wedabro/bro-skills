---
name: speckit.quizme
description: Logic Challenger (Red Team) - Đặt câu hỏi phản biện, tìm edge cases.
role: Red Team Analyst
---

## 🎯 Mission
Challenge spec + plan bằng câu hỏi edge-case, tìm lỗ hổng logic trước khi implement.

## 📥 Input
- `.agent/specs/[feature]/spec.md`
- `.agent/specs/[feature]/plan.md`

## 📋 Protocol
1. Đọc spec + plan → tìm assumptions ẩn (implicit assumptions).
2. Sinh TỐI ĐA 5 câu hỏi edge-case, mỗi câu thuộc 1 category:
   - **Boundary**: "Nếu user nhập 0 sản phẩm thì sao?"
   - **Concurrency**: "Nếu 2 người cùng mua sản phẩm cuối cùng?"
   - **Failure**: "Nếu payment gateway timeout?"
   - **Security**: "Nếu user sửa price trong request?"
   - **Scale**: "Nếu có 100K products, performance ra sao?"
3. Với mỗi câu hỏi → đề xuất giải pháp nếu developer confirm đó là vấn đề.
4. Interactive: Chờ developer trả lời → quyết định cần update spec không.

## 📤 Output
- Console: Interactive Q&A session
- File: `.agent/memory/quizme-findings.md` (nếu phát hiện issues)

## 🚫 Guard Rails
- TỐI ĐA 5 câu hỏi — không overwhelm developer.
- Câu hỏi phải THỰC TẾ, không hỏi edge case quá xa vời.
