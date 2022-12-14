from dataclasses import dataclass
from typing import Any, Type

from matplotlib import pyplot as plt
from reprep import Report, MIME_PDF

from pdm4ar.exercises_def.ex04.map import map2image
from pdm4ar.exercises.ex04.mdp import GridMdpSolver
from pdm4ar.exercises.ex04.policy_iteration import PolicyIteration
from pdm4ar.exercises.ex04.value_iteration import ValueIteration
from pdm4ar.exercises_def import Exercise, ExIn
from pdm4ar.exercises_def.ex04.data import get_test_grids
from pdm4ar.exercises_def.ex04.utils import action2arrow, head_width


@dataclass
class TestValueEx4(ExIn):
    algo: Type[GridMdpSolver]

    def str_id(self) -> str:
        return str(self.algo.__name__)


def exercise4_report(ex_in: TestValueEx4, ex_out=None) -> Report:
    r = Report("Ex4-ValueAndPolicyIteration")

    for k, grid_mdp in enumerate(get_test_grids()):
        solver: GridMdpSolver = ex_in.algo()
        algo_name = solver.__class__.__name__
        value_func, policy = solver.solve(grid_mdp)

        MAP_SHAPE = grid_mdp.grid.shape
        font_size = 3 if MAP_SHAPE[0] > 15 else 6

        rfig = r.figure(cols=2)
        with rfig.plot(nid=f"{algo_name}-value-{k}", mime=MIME_PDF, figsize=None) as _:
            ax = plt.gca()
            ax.imshow(value_func, aspect="equal")
            ax.tick_params(axis="both", labelsize=font_size + 3)
            for i in range(MAP_SHAPE[0]):
                for j in range(MAP_SHAPE[1]):
                    ax.text(j, i, f"{value_func[i, j]:.1f}", size=font_size, ha="center", va="center", color="k")

        map_c = map2image(grid_mdp.grid)
        with rfig.plot(nid=f"{algo_name}-policy-{k}", mime=MIME_PDF, figsize=None) as _:
            ax = plt.gca()
            ax.imshow(map_c, aspect="equal")
            ax.tick_params(axis="both", labelsize=font_size + 3)
            for i in range(MAP_SHAPE[0]):
                for j in range(MAP_SHAPE[1]):
                    arrow = action2arrow[policy[i, j]]
                    ax.arrow(j, i, arrow[1], arrow[0], head_width=head_width, color="k")
    return r


def algo_placeholder(ex_in):
    return None


def get_exercise4() -> Exercise:
    test_values = [TestValueEx4(ValueIteration), TestValueEx4(PolicyIteration)]
    return Exercise[TestValueEx4, Any](
        desc="This exercise is about value and policy iteration",
        algorithm=algo_placeholder,
        evaluation_fun=exercise4_report,
        test_values=test_values,
    )
