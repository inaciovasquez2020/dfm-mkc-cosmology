#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DNP = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

OBJECTS = [
    {
        "object_id": "AUTHENTIC_EXTERNAL_DATA_PAYLOAD",
        "status": "AUTHENTIC_EXTERNAL_DATA_PAYLOAD_BLOCKED_NO_PAYLOAD_SUPPLIED",
        "check_result": "BLOCKED_NO_PAYLOAD_SUPPLIED",
        "preserved": "AUTHENTIC_EXTERNAL_DATA_PAYLOAD_NOT_BOUND",
        "terminal": "EXTERNAL_EMPIRICAL_PAYLOAD_NOT_SUPPLIED",
        "missing": [
            "EXTERNAL_PAYLOAD_FILE",
            "EXTERNAL_PAYLOAD_SOURCE_RECORD",
            "EXTERNAL_PAYLOAD_LICENSE_RECORD",
            "EXTERNAL_PAYLOAD_DIGEST_LOCK"
        ],
        "false_flags": [
            "authentic_external_data_payload_supplied",
            "external_payload_bound",
            "empirical_validation_claimed",
            "model_selection_claimed"
        ],
        "boundary": [
            "records that authentic external empirical payload is blocked",
            "does not supply an external payload file",
            "does not bind an external empirical payload",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_SLOT_BINDING_MAP",
        "status": "PAYLOAD_SLOT_BINDING_MAP_BLOCKED_NO_AUTHENTIC_PAYLOAD",
        "check_result": "BLOCKED_NO_AUTHENTIC_PAYLOAD",
        "preserved": "PAYLOAD_SLOT_BINDING_MAP_NOT_SUPPLIED",
        "terminal": "AUTHENTIC_EXTERNAL_DATA_PAYLOAD_NOT_SUPPLIED",
        "missing": [
            "AUTHENTIC_EXTERNAL_DATA_PAYLOAD",
            "PAYLOAD_COLUMN_MAP",
            "PAYLOAD_SLOT_INDEX_MAP",
            "PAYLOAD_SCHEMA_VALIDATION_RESULT"
        ],
        "false_flags": [
            "payload_slot_binding_map_supplied",
            "external_payload_bound",
            "empirical_values_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that payload slot binding is blocked",
            "does not map empirical payload columns to schema slots",
            "does not bind empirical values to slots",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_DIGEST_LOCK",
        "status": "PAYLOAD_DIGEST_LOCK_BLOCKED_NO_PAYLOAD_BYTES",
        "check_result": "BLOCKED_NO_PAYLOAD_BYTES",
        "preserved": "PAYLOAD_DIGEST_LOCK_NOT_SUPPLIED",
        "terminal": "EXTERNAL_PAYLOAD_BYTES_NOT_SUPPLIED",
        "missing": [
            "EXTERNAL_PAYLOAD_BYTES",
            "SHA256_PAYLOAD_DIGEST",
            "PAYLOAD_VERSION_RECORD"
        ],
        "false_flags": [
            "payload_digest_lock_supplied",
            "external_payload_bound",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that payload digest locking is blocked",
            "does not hash external payload bytes",
            "does not freeze an empirical payload version",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "EMPIRICAL_VALUE_ARRAY",
        "status": "EMPIRICAL_VALUE_ARRAY_BLOCKED_NO_PAYLOAD_SLOT_BINDING",
        "check_result": "BLOCKED_NO_PAYLOAD_SLOT_BINDING",
        "preserved": "EMPIRICAL_VALUE_ARRAY_NOT_SUPPLIED",
        "terminal": "PAYLOAD_SLOT_BINDING_MAP_NOT_SUPPLIED",
        "missing": [
            "PAYLOAD_SLOT_BINDING_MAP",
            "EMPIRICAL_SLOT_VALUE_EXTRACTION",
            "EMPIRICAL_VALUE_ARRAY_DIGEST_LOCK"
        ],
        "false_flags": [
            "empirical_value_array_supplied",
            "empirical_values_supplied",
            "empirical_validation_claimed",
            "model_selection_claimed"
        ],
        "boundary": [
            "records that empirical value extraction is blocked",
            "does not extract empirical data values",
            "does not populate the data vector schema",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "EMPIRICAL_UNCERTAINTY_ARRAY",
        "status": "EMPIRICAL_UNCERTAINTY_ARRAY_BLOCKED_NO_PAYLOAD_SLOT_BINDING",
        "check_result": "BLOCKED_NO_PAYLOAD_SLOT_BINDING",
        "preserved": "EMPIRICAL_UNCERTAINTY_ARRAY_NOT_SUPPLIED",
        "terminal": "PAYLOAD_SLOT_BINDING_MAP_NOT_SUPPLIED",
        "missing": [
            "PAYLOAD_SLOT_BINDING_MAP",
            "EMPIRICAL_UNCERTAINTY_EXTRACTION",
            "EMPIRICAL_UNCERTAINTY_ARRAY_DIGEST_LOCK"
        ],
        "false_flags": [
            "empirical_uncertainty_array_supplied",
            "observational_uncertainties_supplied",
            "empirical_validation_claimed",
            "model_selection_claimed"
        ],
        "boundary": [
            "records that empirical uncertainty extraction is blocked",
            "does not extract observational uncertainties",
            "does not populate uncertainty slots",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "BACKGROUND_NUMERICAL_SOLVER_RUN",
        "status": "BACKGROUND_NUMERICAL_SOLVER_RUN_BLOCKED_NO_SOLVER_IMPLEMENTATION",
        "check_result": "BLOCKED_NO_SOLVER_IMPLEMENTATION",
        "preserved": "BACKGROUND_NUMERICAL_SOLVER_RUN_NOT_SUPPLIED",
        "terminal": "BACKGROUND_SOLVER_IMPLEMENTATION_NOT_SUPPLIED",
        "missing": [
            "BACKGROUND_SOLVER_IMPLEMENTATION",
            "BACKGROUND_SOLVER_CONFIGURATION",
            "BACKGROUND_SOLVER_OUTPUT_ARRAY",
            "BACKGROUND_SOLVER_DIGEST_LOCK"
        ],
        "false_flags": [
            "background_solver_run_supplied",
            "background_numerical_integration_executed",
            "prediction_values_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that background numerical solver execution is blocked",
            "does not execute background numerical integration",
            "does not produce background prediction values",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PERTURBATION_NUMERICAL_SOLVER_RUN",
        "status": "PERTURBATION_NUMERICAL_SOLVER_RUN_BLOCKED_NO_SOLVER_IMPLEMENTATION",
        "check_result": "BLOCKED_NO_SOLVER_IMPLEMENTATION",
        "preserved": "PERTURBATION_NUMERICAL_SOLVER_RUN_NOT_SUPPLIED",
        "terminal": "PERTURBATION_SOLVER_IMPLEMENTATION_NOT_SUPPLIED",
        "missing": [
            "PERTURBATION_SOLVER_IMPLEMENTATION",
            "PERTURBATION_SOLVER_CONFIGURATION",
            "PERTURBATION_SOLVER_OUTPUT_ARRAY",
            "PERTURBATION_SOLVER_DIGEST_LOCK"
        ],
        "false_flags": [
            "perturbation_solver_run_supplied",
            "perturbation_numerical_integration_executed",
            "prediction_values_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that perturbation numerical solver execution is blocked",
            "does not execute perturbation numerical integration",
            "does not produce growth prediction values",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "TRANSFER_FUNCTION_SOLVER_RUN",
        "status": "TRANSFER_FUNCTION_SOLVER_RUN_BLOCKED_NO_TRANSFER_SOLVER_IMPLEMENTATION",
        "check_result": "BLOCKED_NO_TRANSFER_SOLVER_IMPLEMENTATION",
        "preserved": "TRANSFER_FUNCTION_SOLVER_RUN_NOT_SUPPLIED",
        "terminal": "TRANSFER_FUNCTION_SOLVER_IMPLEMENTATION_NOT_SUPPLIED",
        "missing": [
            "TRANSFER_FUNCTION_SOLVER_IMPLEMENTATION",
            "RECOMBINATION_CLOSURE",
            "TRANSFER_FUNCTION_OUTPUT_ARRAY",
            "TRANSFER_FUNCTION_DIGEST_LOCK"
        ],
        "false_flags": [
            "transfer_function_solver_run_supplied",
            "boltzmann_transfer_executed",
            "cmb_prediction_values_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that transfer-function solver execution is blocked",
            "does not execute Boltzmann or transfer-function computation",
            "does not produce CMB spectrum prediction values",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PREDICTION_VALUE_ARRAY",
        "status": "PREDICTION_VALUE_ARRAY_BLOCKED_NO_SOLVER_OUTPUTS",
        "check_result": "BLOCKED_NO_SOLVER_OUTPUTS",
        "preserved": "PREDICTION_VALUE_ARRAY_NOT_SUPPLIED",
        "terminal": "SOLVER_OUTPUT_ARRAYS_NOT_SUPPLIED",
        "missing": [
            "BACKGROUND_SOLVER_OUTPUT_ARRAY",
            "PERTURBATION_SOLVER_OUTPUT_ARRAY",
            "TRANSFER_FUNCTION_OUTPUT_ARRAY",
            "PREDICTION_SLOT_ASSEMBLY_MAP"
        ],
        "false_flags": [
            "prediction_value_array_supplied",
            "executable_prediction_values_supplied",
            "likelihood_ready_predictions_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that prediction value assembly is blocked",
            "does not assemble executable DFM prediction values",
            "does not populate model prediction slots",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PREDICTION_RUN_DIGEST_LOCK",
        "status": "PREDICTION_RUN_DIGEST_LOCK_BLOCKED_NO_PREDICTION_RUN_OUTPUTS",
        "check_result": "BLOCKED_NO_PREDICTION_RUN_OUTPUTS",
        "preserved": "PREDICTION_RUN_DIGEST_LOCK_NOT_SUPPLIED",
        "terminal": "PREDICTION_RUN_OUTPUTS_NOT_SUPPLIED",
        "missing": [
            "PREDICTION_RUN_OUTPUT_BYTES",
            "PREDICTION_RUN_SHA256_DIGEST",
            "PREDICTION_RUN_REPRODUCTION_COMMAND"
        ],
        "false_flags": [
            "prediction_run_digest_lock_supplied",
            "prediction_values_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that prediction run digest locking is blocked",
            "does not hash prediction run outputs",
            "does not freeze a prediction run",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_COVARIANCE_ARRAY",
        "status": "PAYLOAD_COVARIANCE_ARRAY_BLOCKED_NO_EMPIRICAL_COVARIANCE_PAYLOAD",
        "check_result": "BLOCKED_NO_EMPIRICAL_COVARIANCE_PAYLOAD",
        "preserved": "PAYLOAD_COVARIANCE_ARRAY_NOT_SUPPLIED",
        "terminal": "EMPIRICAL_COVARIANCE_PAYLOAD_NOT_SUPPLIED",
        "missing": [
            "EMPIRICAL_COVARIANCE_PAYLOAD",
            "PAYLOAD_COVARIANCE_SLOT_ORDER",
            "PAYLOAD_COVARIANCE_DIGEST_LOCK"
        ],
        "false_flags": [
            "payload_covariance_array_supplied",
            "payload_bound_covariance_supplied",
            "empirical_covariance_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that empirical covariance array extraction is blocked",
            "does not supply payload-bound covariance values",
            "does not claim empirical covariance",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_COVARIANCE_SLOT_ORDER",
        "status": "PAYLOAD_COVARIANCE_SLOT_ORDER_BLOCKED_NO_COVARIANCE_PAYLOAD",
        "check_result": "BLOCKED_NO_COVARIANCE_PAYLOAD",
        "preserved": "PAYLOAD_COVARIANCE_SLOT_ORDER_NOT_SUPPLIED",
        "terminal": "EMPIRICAL_COVARIANCE_PAYLOAD_NOT_SUPPLIED",
        "missing": [
            "EMPIRICAL_COVARIANCE_PAYLOAD",
            "COVARIANCE_PAYLOAD_SLOT_MAP",
            "COVARIANCE_SCHEMA_ALIGNMENT_CHECK"
        ],
        "false_flags": [
            "payload_covariance_slot_order_supplied",
            "payload_bound_covariance_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that covariance slot-order binding is blocked",
            "does not align empirical covariance to schema order",
            "does not supply payload-bound covariance",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_COVARIANCE_DIGEST_LOCK",
        "status": "PAYLOAD_COVARIANCE_DIGEST_LOCK_BLOCKED_NO_COVARIANCE_BYTES",
        "check_result": "BLOCKED_NO_COVARIANCE_BYTES",
        "preserved": "PAYLOAD_COVARIANCE_DIGEST_LOCK_NOT_SUPPLIED",
        "terminal": "COVARIANCE_PAYLOAD_BYTES_NOT_SUPPLIED",
        "missing": [
            "COVARIANCE_PAYLOAD_BYTES",
            "COVARIANCE_SHA256_DIGEST",
            "COVARIANCE_VERSION_RECORD"
        ],
        "false_flags": [
            "payload_covariance_digest_lock_supplied",
            "payload_bound_covariance_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that covariance digest locking is blocked",
            "does not hash covariance payload bytes",
            "does not freeze covariance payload version",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "PAYLOAD_COVARIANCE_POSITIVE_DEFINITE_CHECK",
        "status": "PAYLOAD_COVARIANCE_POSITIVE_DEFINITE_CHECK_BLOCKED_NO_PAYLOAD_COVARIANCE_ARRAY",
        "check_result": "BLOCKED_NO_PAYLOAD_COVARIANCE_ARRAY",
        "preserved": "PAYLOAD_COVARIANCE_POSITIVE_DEFINITE_CHECK_NOT_SUPPLIED",
        "terminal": "PAYLOAD_COVARIANCE_ARRAY_NOT_SUPPLIED",
        "missing": [
            "PAYLOAD_COVARIANCE_ARRAY",
            "COVARIANCE_SYMMETRY_CHECK",
            "COVARIANCE_POSITIVE_DEFINITE_CERTIFICATE"
        ],
        "false_flags": [
            "payload_covariance_positive_definite_check_supplied",
            "positive_definite_payload_covariance_claimed",
            "payload_bound_covariance_supplied",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that payload covariance positive-definite checking is blocked",
            "does not prove covariance positive definiteness",
            "does not supply payload-bound covariance",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "DFM_CHI_SQUARE_VALUE",
        "status": "DFM_CHI_SQUARE_VALUE_BLOCKED_NO_LIKELIHOOD_EXECUTION_INPUTS",
        "check_result": "BLOCKED_NO_LIKELIHOOD_EXECUTION_INPUTS",
        "preserved": "DFM_CHI_SQUARE_VALUE_NOT_SUPPLIED",
        "terminal": "EMPIRICAL_DATA_AND_PREDICTION_VALUES_NOT_SUPPLIED",
        "missing": [
            "EMPIRICAL_VALUE_ARRAY",
            "PREDICTION_VALUE_ARRAY",
            "PAYLOAD_BOUND_COVARIANCE_MATRIX",
            "EXECUTED_DFM_CHI_SQUARE_COMPUTATION"
        ],
        "false_flags": [
            "dfm_chi_square_supplied",
            "likelihood_executed",
            "model_selection_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that DFM chi-square computation is blocked",
            "does not compute a DFM chi-square value",
            "does not execute the likelihood",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "LAMBDA_CDM_CHI_SQUARE_VALUE",
        "status": "LAMBDA_CDM_CHI_SQUARE_VALUE_BLOCKED_NO_LIKELIHOOD_EXECUTION_INPUTS",
        "check_result": "BLOCKED_NO_LIKELIHOOD_EXECUTION_INPUTS",
        "preserved": "LAMBDA_CDM_CHI_SQUARE_VALUE_NOT_SUPPLIED",
        "terminal": "EMPIRICAL_DATA_AND_BASELINE_VALUES_NOT_SUPPLIED",
        "missing": [
            "EMPIRICAL_VALUE_ARRAY",
            "PAYLOAD_BOUND_COVARIANCE_MATRIX",
            "LAMBDA_CDM_PAYLOAD_ALIGNED_BASELINE",
            "EXECUTED_LAMBDA_CDM_CHI_SQUARE_COMPUTATION"
        ],
        "false_flags": [
            "lambda_cdm_chi_square_supplied",
            "likelihood_executed",
            "model_selection_claimed",
            "lambda_cdm_failure_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that Lambda-CDM chi-square computation is blocked",
            "does not compute a Lambda-CDM chi-square value",
            "does not claim Lambda-CDM failure",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "DELTA_CHI_SQUARE_VALUE",
        "status": "DELTA_CHI_SQUARE_VALUE_BLOCKED_NO_COMPONENT_CHI_SQUARE_VALUES",
        "check_result": "BLOCKED_NO_COMPONENT_CHI_SQUARE_VALUES",
        "preserved": "DELTA_CHI_SQUARE_VALUE_NOT_SUPPLIED",
        "terminal": "DFM_AND_LAMBDA_CDM_CHI_SQUARE_VALUES_NOT_SUPPLIED",
        "missing": [
            "DFM_CHI_SQUARE_VALUE",
            "LAMBDA_CDM_CHI_SQUARE_VALUE",
            "DELTA_CHI_SQUARE_COMPUTATION"
        ],
        "false_flags": [
            "delta_chi_square_supplied",
            "likelihood_executed",
            "model_selection_claimed",
            "lambda_cdm_failure_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that delta chi-square computation is blocked",
            "does not compute model-comparison statistics",
            "does not claim model selection",
            "does not claim Lambda-CDM failure",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "EXECUTED_LIKELIHOOD_DIGEST_LOCK",
        "status": "EXECUTED_LIKELIHOOD_DIGEST_LOCK_BLOCKED_NO_EXECUTED_LIKELIHOOD_RESULT",
        "check_result": "BLOCKED_NO_EXECUTED_LIKELIHOOD_RESULT",
        "preserved": "EXECUTED_LIKELIHOOD_DIGEST_LOCK_NOT_SUPPLIED",
        "terminal": "EXECUTED_LIKELIHOOD_RESULT_NOT_SUPPLIED",
        "missing": [
            "EXECUTED_LIKELIHOOD_RESULT",
            "LIKELIHOOD_OUTPUT_BYTES",
            "LIKELIHOOD_OUTPUT_SHA256_DIGEST"
        ],
        "false_flags": [
            "executed_likelihood_digest_lock_supplied",
            "likelihood_executed",
            "model_selection_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that executed likelihood digest locking is blocked",
            "does not hash likelihood execution outputs",
            "does not freeze likelihood execution results",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "HOLDOUT_PAYLOAD_DIGEST_LOCK",
        "status": "HOLDOUT_PAYLOAD_DIGEST_LOCK_BLOCKED_NO_HOLDOUT_PAYLOAD_BYTES",
        "check_result": "BLOCKED_NO_HOLDOUT_PAYLOAD_BYTES",
        "preserved": "HOLDOUT_PAYLOAD_DIGEST_LOCK_NOT_SUPPLIED",
        "terminal": "HOLDOUT_PAYLOAD_BYTES_NOT_SUPPLIED",
        "missing": [
            "HOLDOUT_PAYLOAD_BYTES",
            "HOLDOUT_PAYLOAD_SHA256_DIGEST",
            "HOLDOUT_PAYLOAD_SOURCE_RECORD"
        ],
        "false_flags": [
            "holdout_payload_digest_lock_supplied",
            "holdout_payload_bound",
            "holdout_survival_claimed",
            "empirical_validation_claimed"
        ],
        "boundary": [
            "records that holdout payload digest locking is blocked",
            "does not hash holdout payload bytes",
            "does not bind a holdout payload",
            "does not claim holdout survival",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "REPRODUCTION_COMMANDS",
        "status": "REPRODUCTION_COMMANDS_BLOCKED_NO_EXECUTABLE_PIPELINE",
        "check_result": "BLOCKED_NO_EXECUTABLE_PIPELINE",
        "preserved": "REPRODUCTION_COMMANDS_NOT_SUPPLIED",
        "terminal": "EXECUTABLE_PIPELINE_NOT_SUPPLIED",
        "missing": [
            "PIPELINE_ENTRYPOINT",
            "EMPIRICAL_PAYLOAD_BINDING_COMMAND",
            "PREDICTION_EXECUTION_COMMAND",
            "LIKELIHOOD_EXECUTION_COMMAND"
        ],
        "false_flags": [
            "reproduction_commands_supplied",
            "pipeline_executable_claimed",
            "empirical_validation_claimed",
            "model_selection_claimed"
        ],
        "boundary": [
            "records that reproduction commands are blocked",
            "does not supply executable empirical pipeline commands",
            "does not execute the likelihood",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "REPRODUCTION_LOG",
        "status": "REPRODUCTION_LOG_BLOCKED_NO_REPRODUCTION_COMMANDS_OR_EXECUTION",
        "check_result": "BLOCKED_NO_REPRODUCTION_COMMANDS_OR_EXECUTION",
        "preserved": "REPRODUCTION_LOG_NOT_SUPPLIED",
        "terminal": "REPRODUCTION_COMMANDS_AND_EXECUTION_NOT_SUPPLIED",
        "missing": [
            "REPRODUCTION_COMMANDS",
            "REPRODUCTION_RUN_OUTPUT",
            "REPRODUCTION_RUN_DIGEST_LOCK"
        ],
        "false_flags": [
            "reproduction_log_supplied",
            "reproduction_executed",
            "empirical_validation_claimed",
            "model_selection_claimed"
        ],
        "boundary": [
            "records that reproduction logging is blocked",
            "does not supply a reproduction log",
            "does not execute a reproduction run",
            "does not supply empirical evidence"
        ],
    },
    {
        "object_id": "CLAIM_BOUNDARY_AUDIT",
        "status": "CLAIM_BOUNDARY_AUDIT_SUPPLIED_TERMINAL_NO_EMPIRICAL_CLAIM",
        "check_result": "PASS_TERMINAL_NO_EMPIRICAL_CLAIM_AUDIT",
        "preserved": "CLAIM_BOUNDARY_AUDIT_NOT_SUPPLIED",
        "terminal": "NO_EMPIRICAL_CLAIM_PERMITTED_WITHOUT_PAYLOAD_AND_EXECUTION",
        "missing": [
            "EMPIRICAL_DATA_VALUES",
            "EXECUTABLE_DFM_PREDICTION_VALUES",
            "PAYLOAD_BOUND_COVARIANCE_MATRIX",
            "EXECUTED_LIKELIHOOD_RESULT",
            "REPRODUCIBLE_HOLDOUT_REPORT"
        ],
        "false_flags": [
            "dfm_mkc_validated_claimed",
            "lambda_cdm_failure_claimed",
            "holdout_survival_claimed",
            "empirical_validation_claimed",
            "model_selection_claimed",
            "nobel_level_discovery_claimed"
        ],
        "boundary": [
            "supplies a terminal no-empirical-claim audit",
            "confirms empirical validation remains blocked",
            "does not claim DFM-MKC validation",
            "does not claim Lambda-CDM failure",
            "does not claim holdout survival",
            "does not supply empirical evidence"
        ],
    },
]

for item in OBJECTS:
    spec = {
        "object_id": item["object_id"],
        "status": item["status"],
        "date": "2026-05-22",
        "input_specs": [
            "specs/DATA_VECTOR_SCHEMA.json",
            "specs/COVARIANCE_MATRIX.json",
            "specs/LIKELIHOOD_RULE.json",
            "specs/LAMBDA_CDM_BASELINE_VECTOR.json",
            "specs/INDEPENDENT_EMPIRICAL_VALIDATION.json",
            "specs/EMPIRICAL_DATA_VALUES.json",
            "specs/EXECUTABLE_DFM_PREDICTION_VALUES.json",
            "specs/PAYLOAD_BOUND_COVARIANCE_MATRIX.json",
            "specs/EXECUTED_LIKELIHOOD_RESULT.json",
            "specs/REPRODUCIBLE_HOLDOUT_REPORT.json"
        ],
        "blocked_reason": item["terminal"],
        "blocking_missing_objects": item["missing"],
        "check_result": item["check_result"],
        "does_not_prove": DNP,
        "next_missing_objects": item["missing"],
    }
    for flag in item["false_flags"]:
        spec[flag] = False
    (ROOT / "specs" / f"{item['object_id']}.json").write_text(json.dumps(spec, indent=2) + "\n")

    slug = item["object_id"].lower()
    artifact = {
        "artifact_id": f"{slug}_2026_05_22",
        "status": item["status"],
        "required_object_blocked": item["object_id"],
        "source_spec": f"specs/{item['object_id']}.json",
        "root_blocker_preserved": item["preserved"],
        "terminal_blocker": item["terminal"],
        "check_result": item["check_result"],
        "boundary": item["boundary"],
        "does_not_prove": DNP,
        "next_missing_objects": item["missing"],
    }
    (ROOT / "artifacts" / "repo_intake" / f"{slug}_2026_05_22.json").write_text(json.dumps(artifact, indent=2) + "\n")

    title = item["object_id"].replace("_", " ").title()
    md = [
        f"# {title}",
        "",
        f"Status: `{item['status']}`",
        "",
        "Required object blocked:",
        "",
        f"- `{item['object_id']}`",
        "",
        "Root blocker preserved:",
        "",
        f"- `{item['preserved']}`",
        "",
        "Terminal blocker:",
        "",
        f"- `{item['terminal']}`",
        "",
        "Check result:",
        "",
        f"- `{item['check_result']}`",
        "",
        "Boundary:",
        "",
    ]
    md += [f"- {x}" for x in item["boundary"]]
    md += ["", "Does not prove:", ""]
    md += [f"- {x}" for x in DNP]
    md += ["", "Next missing objects:", ""]
    md += [f"- `{x}`" for x in item["missing"]]
    (ROOT / "docs" / "status" / f"{item['object_id']}_2026_05_22.md").write_text("\n".join(md) + "\n")

print(f"Generated {len(OBJECTS)} remaining empirical payload blocker objects.")
