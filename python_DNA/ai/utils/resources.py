import random
import numpy as np
import re


def make_sequence_problem():
    a1 = random.randint(2, 10)
    d = random.randint(2, 5)
    r = random.randint(2, 4)
    n = random.randint(5, 12)
    sn = n * (2*a1 + (n-1)*d)//2
    an = a1 * r**(n-1)
    latex = [
        f"a_1={a1}", f"d={d}", f"n={n}",
        f"\\text{{등차수열 합}}~S_n={sn}", f"\\text{{n번째 등비항}}~a_n={an}"
    ]
    explain = "a_n은 등차, 등비 혼합수열의 일반항/합"
    answer = {"Sn": sn, "an": an}
    return dict(type="수열", latex=latex[:3], answer=answer, explain=explain)

def make_integer_problem():
    while True:
        x = random.randint(2, 20)
        y = random.randint(x+1, x+10)
        z = random.randint(y+1, y+10)
        if np.gcd.reduce([x, y, z]) == 1:
            break
    s = x + y + z
    p = x * y * z
    latex = [f"x+y+z={s}", f"xyz={p}", f"x<y<z"]
    explain = "x, y, z는 서로소인 양의 정수"
    answer = (x, y, z)
    return dict(type="정수", latex=latex, answer=answer, explain=explain)

def make_geometry_problem():
    r = random.randint(5, 15)
    theta = random.choice([60, 90, 120])
    arc = round(2*np.pi*r*(theta/360), 2)
    area = round(np.pi*(r**2)*(theta/360), 2)
    latex = [f"반지름~r={r}", f"중심각~{theta}^\\circ", f"호의~길이~L={arc}"]
    explain = "원의 부채꼴 넓이, 호의 길이"
    answer = {"arc": arc, "area": area}
    return dict(type="기하", latex=latex, answer=answer, explain=explain)

def make_trigonometry_problem():
    a = random.choice([30, 45, 60, 75, 120])
    b = random.choice([15, 45, 90])
    expr = f"sin({a}^\\circ)cos({b}^\\circ) + cos({a}^\\circ)sin({b}^\\circ)"
    value = round(np.sin(np.deg2rad(a+b)), 3)
    latex = [f"sin({a}^\\circ)", f"sin({b}^\\circ)", f"{expr}"]
    explain = "삼각함수의 합 공식, 변형"
    answer = value
    return dict(type="삼각함수", latex=latex, answer=answer, explain=explain)

def make_calculus_problem():
    a = random.randint(1, 5)
    b = random.randint(-4, 4)
    c = random.randint(-6, 6)
    l = random.randint(1, 3)
    r = l + random.randint(2, 5)
    integral = (a/3)*(r**3-l**3)+(b/2)*(r**2-l**2)+c*(r-l)
    latex = [f"f(x)={a}x^2{b:+}x{c:+}", f"구간~[{l},{r}]", f"\\int_{{{l}}}^{{{r}}} f(x) dx"]
    explain = "정적분, 2차함수 면적"
    answer = round(integral,3)
    return dict(type="미적분", latex=latex, answer=answer, explain=explain)

def make_probability_problem():
    n = random.randint(4, 7)
    k = random.randint(1, n)
    from math import comb
    prob = round(comb(n, k) / 2 ** n, 4)
    latex = [f"동전~{n}번~던짐", f"앞면~{k}번~나옴", f"P={prob}"]
    explain = "이항분포, 경우의 수"
    answer = prob
    return dict(type="확률", latex=latex, answer=answer, explain=explain)

def make_statistics_problem():
    scores = [random.randint(40, 100) for _ in range(7)]
    avg = round(sum(scores)/len(scores),2)
    std = round(np.std(scores, ddof=1),2)
    latex = [f"점수:~{',~'.join(map(str,scores))}", f"평균~\\bar{{x}}={avg}", f"표준편차~s={std}"]
    explain = "표본 평균, 표본 표준편차"
    answer = {"mean": avg, "std": std}
    return dict(type="통계", latex=latex, answer=answer, explain=explain)

def make_log_problem():
    a = random.randint(2, 5)
    b = random.randint(2, 7)
    c = random.randint(1, 4)
    value = round(np.log(a**b)/np.log(c), 4)
    latex = [f"log_{{{c}}}({a}^{b})", f"밑변환공식~활용", f"값={value}"]
    explain = "로그 밑변환, 거듭제곱"
    answer = value
    return dict(type="로그", latex=latex, answer=answer, explain=explain)

def make_exponential_problem():
    a = random.randint(2, 5)
    b = random.randint(2, 4)
    value = a**b
    latex = [f"{a}^{b}", f"지수~계산", f"값={value}"]
    explain = "지수법칙 활용"
    answer = value
    return dict(type="지수", latex=latex, answer=answer, explain=explain)

def make_quadratic_function_problem():
    a = random.randint(1, 4)
    b = random.randint(-7, 7)
    c = random.randint(-10, 10)
    vx = -b/(2*a)
    vy = a*vx**2 + b*vx + c
    latex = [f"y={a}x^2{b:+}x{c:+}", f"꼭짓점~좌표", f"({round(vx,2)},~{round(vy,2)})"]
    explain = "이차함수의 꼭짓점"
    answer = (round(vx,2), round(vy,2))
    return dict(type="이차함수", latex=latex, answer=answer, explain=explain)

def make_quadratic_equation_problem():
    a = random.randint(1, 5)
    b = random.randint(-7, 7)
    c = random.randint(-7, 7)
    d = b**2 - 4*a*c
    if d < 0: c = b**2 // (4*a)
    roots = np.roots([a, b, c])
    roots = [round(float(r),2) for r in roots]
    latex = [f"{a}x^2{b:+}x{c:+}=0", f"근의~공식", f"근={roots}"]
    explain = "이차방정식의 근"
    answer = roots
    return dict(type="이차방정식", latex=latex, answer=answer, explain=explain)

PROBLEM_MAKERS = {
    "수열": make_sequence_problem,
    "정수": make_integer_problem,
    "기하": make_geometry_problem,
    "삼각함수": make_trigonometry_problem,
    "미적분": make_calculus_problem,
    "확률": make_probability_problem,
    "통계": make_statistics_problem,
    "로그": make_log_problem,
    "지수": make_exponential_problem,
    "이차함수": make_quadratic_function_problem,
    "이차방정식": make_quadratic_equation_problem,
}

# ----------- 텍스트 처리/문제 유형 분류 등 유틸 -------------
def classify_type_by_text(text):
    for key in PROBLEM_MAKERS.keys():
        if key in text:
            return key
    if re.search(r"수열|합|공차|공비|a_", text): return "수열"
    if re.search(r"정수|gcd|lcm|소수|합성수|integer|solution", text): return "정수"
    if re.search(r"원의|넓이|부채꼴|삼각형|입체|기하", text): return "기하"
    if re.search(r"sin|cos|tan|삼각함수", text): return "삼각함수"
    if re.search(r"미분|적분|\\int|정적분|도함수|미적분", text): return "미적분"
    if re.search(r"확률|경우의 수|동전|주사위|확률", text): return "확률"
    if re.search(r"평균|표준편차|분산|사분위|통계", text): return "통계"
    if re.search(r"log_|로그", text): return "로그"
    if re.search(r"지수|a\^|b\^|c\^", text): return "지수"
    if re.search(r"x\^2|이차함수|꼭짓점", text): return "이차함수"
    if re.search(r"x\^2|=0|이차방정식|근", text): return "이차방정식"
    return "정수"