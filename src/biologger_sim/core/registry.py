import csv
from pathlib import Path


class EcosystemRegistry:
    """
    Registry for managing simulation IDs and mapping them to metadata biological IDs.

    Definitions:
    - eid (int): A compact integer identifier for ZMQ protocol efficiency.
    - sim_id (str): A unique string handle for a simulation instance (e.g., 'sword_r_exact').
                    Used as the primary key for visualization paths and ZMQ payloads.
    - tag_id (str): The biological/deployment identifier (e.g., 'RED001_20220812').
                Used to lookup actual metadata in biologger_meta.csv (species, etc).
    """

    def __init__(self, meta_file: Path | None = None) -> None:
        self._sim_id_to_eid: dict[str, int] = {}
        self._eid_to_sim_id: dict[int, str] = {}
        self._sim_id_to_tag_id: dict[str, str] = {}  # sim_id -> metadata_id
        self._tag_id_to_species: dict[str, str] = {}  # metadata_id -> species
        self._next_eid = 0

        if meta_file and meta_file.exists():
            self._load_metadata(meta_file)

    def _load_metadata(self, meta_file: Path) -> None:
        """Loads species mapping from biologger_meta.csv."""
        try:
            with open(meta_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 'tag_id' is the primary key in CSV, fallback to 'id'
                    tag_id = row.get("tag_id") or row.get("id")
                    species = row.get("species")
                    if tag_id and species:
                        self._tag_id_to_species[tag_id] = species
        except Exception as e:
            print(f"Warning: Failed to load metadata from {meta_file}: {e}")

    def register(self, sim_id: str, tag_id: str | None = None) -> int:
        """
        Registers a simulation instance.

        Args:
            sim_id: The unique display name (e.g. 'Swordfish_v2')
            tag_id: The biological ID for metadata lookup (e.g. 'RED001').
                    Defaults to sim_id if not provided.

        Returns:
            int: The compact 'eid' for ZMQ transmission.
        """
        if sim_id not in self._sim_id_to_eid:
            eid = self._next_eid
            self._sim_id_to_eid[sim_id] = eid
            self._eid_to_sim_id[eid] = sim_id
            self._sim_id_to_tag_id[sim_id] = tag_id or sim_id
            self._next_eid += 1
            return eid
        return self._sim_id_to_eid[sim_id]

    def get_species(self, sim_id: str) -> str:
        """Returns the scientific species name for a simulation instance."""
        tag_id = self._sim_id_to_tag_id.get(sim_id, sim_id)
        return self._tag_id_to_species.get(tag_id, "unknown")

    def get_eid(self, sim_id: str) -> int | None:
        """Returns the 'eid' (int) for a 'sim_id' (str)."""
        return self._sim_id_to_eid.get(sim_id)

    def get_sim_id(self, eid: int) -> str | None:
        """Returns the 'sim_id' (str) for an 'eid' (int)."""
        return self._eid_to_sim_id.get(eid)

    def clear(self) -> None:
        """Clears the registry."""
        self._sim_id_to_eid.clear()
        self._eid_to_sim_id.clear()
        self._sim_id_to_tag_id.clear()
        self._tag_id_to_species.clear()
        self._next_eid = 0
