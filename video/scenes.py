from manim import *
from scenekit import *

LINE = "#2E332F"


def code(s, size=22, color=PRIMARY, **kw):
    esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return MarkupText(f'<span font_features="calt 0, liga 0">{esc}</span>', font=MONO, font_size=size, color=color, **kw)


def square(size=0.5, color=LINE, opacity=0.35):
    sq = RoundedRectangle(corner_radius=0.06, width=size, height=size, color=color, stroke_width=2)
    return sq.set_fill(color, opacity=opacity)


def paint(sq, color, opacity=0.6):
    return sq.animate.set_stroke(color).set_fill(color, opacity=opacity)


def bar(width, color, height=0.34):
    b = Rectangle(width=max(width, 0.04), height=height, color=color, stroke_width=0)
    return b.set_fill(color, opacity=0.8)


def agents(y=0.0, w=2.6):
    return flow(["planner", "generator", "healer"], width=w, gap=0.9, color=NOTE, size=24).move_to([0, y, 0])


class S1Result(Timed):
    def construct(self):
        title = code("npx playwright init-agents", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        hook = VGroup(
            txt("Playwright's test agents wrote our tests", 40),
            code("7 tests in 46 minutes. Would you keep them?", 26, ACCENT),
        ).arrange(DOWN, buff=0.45).move_to([0, 0.3, 0])
        self.play(FadeIn(hook[0], shift=UP * 0.2), run_time=0.5)
        self.at("write your tests")
        self.play(FadeIn(hook[1], shift=UP * 0.15), run_time=0.4)
        first = self.cue("three agents")
        self.cursor = 0
        self.wait(first - 0.6 - self.now())
        self.play(FadeOut(hook), run_time=0.35)

        boxes, arrows = agents(1.9)
        self.at("three agents")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.15), FadeIn(arrows), run_time=0.6)
        tests = VGroup(*[square() for _ in range(7)]).arrange(RIGHT, buff=0.18).move_to([-2.9, -0.2, 0])
        lab = code("7 tests", 22, DIM).next_to(tests, UP, buff=0.25).align_to(tests, LEFT)
        self.at("seven tests")
        self.play(FadeIn(lab), LaggedStart(*[FadeIn(sq, scale=0.6) for sq in tests], lag_ratio=0.06), run_time=0.5)
        mins = code("46 min", 64, ACCENT).move_to([3.4, -0.1, 0])
        self.at("forty six minutes")
        self.play(FadeIn(mins, shift=UP * 0.2), run_time=0.45)
        passed = code("7/7 pass", 22, GOOD).next_to(tests, DOWN, buff=0.25).align_to(tests, LEFT)
        self.at("all seven pass")
        self.play(*[paint(sq, GOOD) for sq in tests], FadeIn(passed), run_time=0.45)
        tease = VGroup(txt("what is good", 30, GOOD), code("·", 26, DIM), txt("what to watch", 30, ACCENT)).arrange(RIGHT, buff=0.3)
        tease.move_to([0, -2.7, 0])
        self.at("here is what is good")
        self.play(FadeIn(tease, shift=UP * 0.15), run_time=0.4)
        self.end()


class S2Setup(Timed):
    def construct(self):
        title = code("the three agents", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        boxes, arrows = agents(1.8)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boxes], lag_ratio=0.15), FadeIn(arrows), run_time=0.6)
        notes = [
            ("the planner", "explores the app,\nwrites a test plan"),
            ("the generator", "writes the tests,\nchecks every locator\nin a live browser"),
            ("the healer", "repairs tests\nthat broke"),
        ]
        for box, (cue, text) in zip(boxes, notes):
            note = code(text, 18, DIM, line_spacing=0.9).next_to(box, DOWN, buff=0.3)
            self.at(cue)
            self.play(light_up(box, GOOD), FadeIn(note, shift=UP * 0.1), run_time=0.4)
        lx = -5.6
        app = code("target   the-internet.herokuapp.com  ·  Playwright 1.62", 22).move_to([lx, -1.7, 0], aligned_edge=LEFT)
        base = code("compare  6 tests written in one pass, no browser", 22, ACCENT).move_to([lx, -2.4, 0], aligned_edge=LEFT)
        self.at("i ran them")
        self.play(FadeIn(app, shift=RIGHT * 0.15), run_time=0.4)
        self.at("compared the result")
        self.play(FadeIn(base, shift=RIGHT * 0.15), run_time=0.4)
        self.end()


class S3Numbers(Timed):
    def construct(self):
        title = code("the numbers", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        lx, bx, scale = -5.6, -3.2, 7.0 / 2602
        p_lab = code("planner", 24).move_to([lx, 2.3, 0], aligned_edge=LEFT)
        p_bar = bar(164 * scale, NOTE).move_to([bx, 2.3, 0], aligned_edge=LEFT)
        p_txt = code("2m 44s", 22, NOTE).next_to(p_bar, RIGHT, buff=0.2)
        g_lab = code("generator", 24).move_to([lx, 1.6, 0], aligned_edge=LEFT)
        g_bar = bar(2602 * scale, ACCENT).move_to([bx, 1.6, 0], aligned_edge=LEFT)
        g_txt = code("43m 22s", 22, ACCENT).next_to(g_bar, RIGHT, buff=0.2)
        self.at("the planner took")
        self.play(FadeIn(p_lab), GrowFromEdge(p_bar, LEFT), FadeIn(p_txt), run_time=0.4)
        self.at("the generator took")
        self.play(FadeIn(g_lab), GrowFromEdge(g_bar, LEFT), FadeIn(g_txt), run_time=0.7)

        fx, ox = -0.4, 2.8
        heads = VGroup(code("one pass", 22, DIM).move_to([fx, 0.5, 0], aligned_edge=LEFT), code("generated", 22, NOTE).move_to([ox, 0.5, 0], aligned_edge=LEFT))
        rows = [("lines of test code", "80", "223", -0.3), ("checks per test", "~2.5", "~9", -1.2), ("tests passing", "6/6", "7/7", -2.1)]
        cells = []
        for name, a, b, y in rows:
            cells.append((
                code(name, 26).move_to([lx, y, 0], aligned_edge=LEFT),
                code(a, 30, PRIMARY).move_to([fx, y, 0], aligned_edge=LEFT),
                code(b, 30, NOTE).move_to([ox, y, 0], aligned_edge=LEFT),
            ))
        self.at("the one pass suite")
        self.play(FadeIn(heads), FadeIn(cells[0][0]), FadeIn(cells[0][1]), run_time=0.4)
        self.at("two hundred and twenty")
        self.play(FadeIn(cells[0][2], scale=1.2), run_time=0.35)
        self.at("the one pass tests")
        self.play(FadeIn(cells[1][0]), FadeIn(cells[1][1]), run_time=0.35)
        self.at("about nine")
        self.play(FadeIn(cells[1][2], scale=1.2), run_time=0.35)
        self.at("both suites pass")
        self.play(FadeIn(cells[2][0]), FadeIn(cells[2][1].set_color(GOOD)), FadeIn(cells[2][2].set_color(GOOD)), run_time=0.4)
        self.end()


class S4Good(Timed):
    def construct(self):
        title = code("what is good  ·  the live browser", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        lx = -5.6
        head = txt("The live browser paid off", 34, GOOD).move_to([lx, 2.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(head, shift=UP * 0.15), run_time=0.4)
        hidden = VGroup(*[code("#loading", 22, DIM) for _ in range(3)]).arrange(RIGHT, buff=0.5).move_to([lx, 1.3, 0], aligned_edge=LEFT)
        tag = code("hidden, left in the page", 18, DIM).next_to(hidden, RIGHT, buff=0.5)
        self.at("one page keeps")
        self.play(LaggedStart(*[FadeIn(h) for h in hidden], lag_ratio=0.15), FadeIn(tag), run_time=0.5)
        fix = code("page.getByText('Wait for it...').filter({ visible: true })", 22, GOOD).move_to([lx, 0.5, 0], aligned_edge=LEFT)
        self.at("targeted the visible")
        self.play(FadeIn(fix, shift=RIGHT * 0.15), hidden.animate.set_opacity(0.4), run_time=0.45)
        step = code("plan:  type into the disabled input", 24).move_to([lx, -0.9, 0], aligned_edge=LEFT)
        hang = code("would hang", 22, BAD).next_to(step, RIGHT, buff=0.5)
        self.at("the plan also")
        self.play(FadeIn(step, shift=RIGHT * 0.15), run_time=0.4)
        self.at("that step would")
        self.play(FadeIn(hang, scale=1.15), run_time=0.35)
        instead = code("await expect(input).toBeDisabled();", 24, GOOD).move_to([lx, -1.8, 0], aligned_edge=LEFT)
        self.at("the generator checked")
        self.play(FadeIn(instead, shift=RIGHT * 0.15), step.animate.set_opacity(0.45), run_time=0.45)
        self.end()


class S5Healer(Timed):
    def construct(self):
        title = code("what to watch  ·  the healer", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        lx = -5.6
        stale = VGroup(*[square(0.45, BAD, 0.6) for _ in range(6)]).arrange(RIGHT, buff=0.16).move_to([lx, 2.2, 0], aligned_edge=LEFT)
        lab = code("6 stale locators in a login test", 22, BAD).next_to(stale, RIGHT, buff=0.5)
        self.at("i gave it")
        self.play(LaggedStart(*[FadeIn(sq, scale=0.6) for sq in stale], lag_ratio=0.06), FadeIn(lab), run_time=0.5)
        done = code("6 of 6 repaired in 1m 55s", 22, GOOD).next_to(stale, RIGHT, buff=0.5)
        self.at("repaired all six")
        self.play(FadeOut(lab), run_time=0.15)
        self.play(*[paint(sq, GOOD) for sq in stale], FadeIn(done), run_time=0.4)
        ids = VGroup(
            code("page.locator('#username')", 24, ACCENT),
            code("page.locator('#password')", 24, ACCENT),
            code("page.locator('#flash')", 24, ACCENT),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([lx, 0.55, 0], aligned_edge=LEFT)
        self.at("look at what")
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.15) for i in ids], lag_ratio=0.15), run_time=0.5)
        note = code("correct ids,\nnot role locators", 22, PRIMARY, line_spacing=0.9).next_to(ids, RIGHT, buff=0.9)
        self.at("not as role")
        self.play(FadeIn(note, shift=UP * 0.1), run_time=0.35)
        btn_text = "getByRole('button', { name: ' Login' })"
        btn = code(btn_text, 24).move_to([lx, -1.0, 0], aligned_edge=LEFT)
        gap = Rectangle(width=0.22, height=0.42, color=BAD, stroke_width=3)
        quote = span(btn, btn_text, "' Login'")[0]
        gap.move_to([quote.get_center()[0] + btn.width / len(btn_text), btn.get_center()[1], 0])
        gap_lab = code("leading space", 20, BAD).next_to(btn, RIGHT, buff=0.5)
        self.at("matched one button")
        self.play(FadeIn(btn, shift=RIGHT * 0.15), run_time=0.4)
        self.at("leading space")
        self.play(Create(gap), FadeIn(gap_lab), run_time=0.4)
        verdict = txt("The healer repairs. It does not improve.", 34, ACCENT).move_to([lx, -2.5, 0], aligned_edge=LEFT)
        self.at("the healer repairs")
        self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.4)
        self.end()


class S6Verdict(Timed):
    def construct(self):
        title = code("when to use them", 22, DIM).to_edge(UP, buff=0.7)
        self.add(title)
        lx = -5.6
        rows = [
            ("so use the planner", "✓  planner + generator: scaffold tests for an app you do not know", GOOD, 2.0),
            ("budget the time", "   budget the time: 46 minutes for 7 tests", DIM, 1.35),
            ("review the checks", "!  review the checks: 9 per test is 9 things to maintain", ACCENT, 0.4),
            ("let the healer", "✓  healer: proposes fixes in a pull request", GOOD, -0.55),
            ("do not let it", "×  healer: silent repair in the pipeline", BAD, -1.2),
        ]
        for cue, text, color, y in rows:
            row = code(text, 22, color).move_to([lx, y, 0], aligned_edge=LEFT)
            self.at(cue)
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.4)
        caveat = code("caveat: one demo app, one run. Measure on your own app.", 22, ACCENT).move_to([lx, -2.6, 0], aligned_edge=LEFT)
        self.at("one caveat")
        self.play(FadeIn(caveat, shift=UP * 0.1), run_time=0.4)
        self.end()


class S7EndCard(Timed):
    DRIFT = 0

    def construct(self):
        # Right half stays empty for YouTube's end-screen elements
        brand = VGroup(Dot(radius=0.1, color=GOOD), code("gary-parker", 24, GOOD)).arrange(RIGHT, buff=0.2)
        brand.move_to([-6.1, 3.0, 0], aligned_edge=LEFT)
        rows = VGroup()
        for key, value in [
            ("SOURCE", "github.com/qa-gary-parker/\npoc-playwright-test-agents"),
            ("WRITE-UP", "garyparker.dev/blog/\nhands-on-with-playwright-test-agents"),
        ]:
            rows.add(VGroup(code(key, 16, DIM), code(value, 24, line_spacing=0.8)).arrange(DOWN, buff=0.18, aligned_edge=LEFT))
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(brand, DOWN, buff=0.9).align_to(brand, LEFT)
        summary = code("test agents: 7 tests, 46 minutes, 7/7 pass", 20, DIM).move_to([-6.1, -3.0, 0], aligned_edge=LEFT)
        self.add(brand, rows, summary)
        self.end(minimum=10.0)
