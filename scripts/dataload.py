import pandas as pd
import os

def merge_synthea_to_narratives(
    data_path="data/synthea-dataset-100/set100/csv",
    output_path="data/processed_narratives/",
):
    # Load the datasets
    # Synthea default filenames are `patients.csv`, `encounters.csv`, etc.
    patients_df = pd.read_csv(os.path.join(data_path, "patients.csv"))
    encounters_df = pd.read_csv(os.path.join(data_path, "encounters.csv"))
    conditions_df = pd.read_csv(os.path.join(data_path, "conditions.csv"))
    medications_df = pd.read_csv(os.path.join(data_path, "medications.csv"))
    procedures_df = pd.read_csv(os.path.join(data_path, "procedures.csv"))

    # Merge datasets to create narratives
    narratives = []
    for _, encounter in encounters_df.iterrows():
        patient_id = encounter["PATIENT"]
        encounter_id = encounter["Id"]
        encounter_start = encounter["START"]
        encounter_reason = encounter.get("REASONDESCRIPTION", "")

        patient_rows = patients_df[patients_df["Id"] == patient_id]
        if patient_rows.empty:
            # Skip encounters that don't have a matching patient row.
            continue
        patient_info = patient_rows.iloc[0]
        
        conditions = conditions_df[conditions_df["ENCOUNTER"] == encounter_id]
        medications = medications_df[medications_df["ENCOUNTER"] == encounter_id]
        procedures = procedures_df[procedures_df["ENCOUNTER"] == encounter_id]

        patient_name = f"{patient_info['FIRST']} {patient_info['LAST']}"
        visit_type = encounter.get("ENCOUNTERCLASS", "")

        diagnoses_list = [str(x).strip() for x in conditions["DESCRIPTION"].dropna().tolist() if str(x).strip()]
        medications_list = [str(x).strip() for x in medications["DESCRIPTION"].dropna().tolist() if str(x).strip()]
        procedures_list = [str(x).strip() for x in procedures["DESCRIPTION"].dropna().tolist() if str(x).strip()]

        diagnoses_block = "\n".join(f"- {x}" for x in diagnoses_list) if diagnoses_list else "None recorded"
        medications_block = "\n".join(f"- {x}" for x in medications_list) if medications_list else "None recorded"
        procedures_block = "\n".join(f"- {x}" for x in procedures_list) if procedures_list else "None recorded"

        narrative = (
            f"CLINICAL ENCOUNTER SUMMARY\n"
            f"Patient: {patient_name} (ID: {patient_id})\n"
            f"Encounter Date: {encounter_start}\n"
            f"Visit Type: {visit_type}\n"
            f"Primary Reason: {encounter_reason}\n\n"
            f"DIAGNOSES:\n{diagnoses_block}\n\n"
            f"MEDICATIONS PRESCRIBED:\n{medications_block}\n\n"
            f"PROCEDURES:\n{procedures_block}"
        )
        
        narratives.append(narrative)

    # Save narratives to output path
    os.makedirs(output_path, exist_ok=True)
    with open(os.path.join(output_path, "synthea_narratives.txt"), "w") as f:
        for narrative in narratives:
            f.write(narrative + "\n\n")
    print(f"Success! Created {len(narratives)} clinical narratives in {output_path}")

if __name__ == "__main__":
    merge_synthea_to_narratives()