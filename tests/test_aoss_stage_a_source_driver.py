import pytest

from scripts.aoss_stage_a import source_driver


def test_candidate_is_bound_to_exact_acp_source() -> None:
    assert source_driver.SOURCE_REPOSITORY == "ndrorchestration/agent-control-plane"
    assert source_driver.SOURCE_COMMIT == "dbab7c1afafec524ce7c18157de2089cafe79c87"
    assert source_driver.DRIVER_STATUS == "CANDIDATE_NON_EXECUTING"


def test_all_sixteen_frozen_recipe_classes_can_be_planned_without_execution() -> None:
    assert len(source_driver.RECIPE_CLASSES) == 16
    plans = [source_driver.plan_recipe(name) for name in source_driver.RECIPE_CLASSES]
    assert [plan.recipe_class for plan in plans] == list(source_driver.RECIPE_CLASSES)
    assert all(plan.source_commit == source_driver.SOURCE_COMMIT for plan in plans)


@pytest.mark.parametrize("recipe_class", ["", "not_frozen", "NORMAL_COMPLETION", None, 7])
def test_unknown_or_malformed_recipe_fails_closed(recipe_class) -> None:
    with pytest.raises(source_driver.SourceDriverBoundaryError, match="SOURCE_DRIVER_RECIPE_NOT_FROZEN"):
        source_driver.plan_recipe(recipe_class)


def test_execution_entrypoint_is_deliberately_rejected() -> None:
    with pytest.raises(source_driver.SourceDriverBoundaryError, match="SOURCE_DRIVER_EXECUTION_NOT_ACCEPTED"):
        source_driver.execute_recipe("normal_completion")
