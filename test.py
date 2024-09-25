import re

# Example input block (replace this with the actual block you're processing)
block_cleaned = r"""
\section*{L0703015}
Câu 5

Trong phản ứng hạt nhân điều nào sau đây không đúng?\\
A. Số nuclon được bảo toàn\\
B. Năng lượng được bảo toàn\\
C. Điện tích được bảo toàn\\
D. Số proton được bảo toàn

\section*{Lời giải của GV Loigiaihay.com}
Trong phản ứng hạt nhân: Không có định luật bảo toàn số proton.
\section*{L0703015}
"""

# Regex pattern to capture the explanation
explanation_match = re.search(
    r"\\section\*\{Lời giải của GV Loigiaihay.com\}(.*?)(?=(Đáp án cần chọn là|\\section\*\{L\d+\}))",
    block_cleaned,
    re.DOTALL
)

# Extract and print the explanation if found
if explanation_match:
    explanation = explanation_match.group(1).strip()
    print("Explanation:", explanation)
else:
    print("No explanation found.")
