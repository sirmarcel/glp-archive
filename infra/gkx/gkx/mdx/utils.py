def get_length(chunk_or_batch):
    if "positions" in chunk_or_batch:
        return len(chunk_or_batch["positions"])
    elif "energy" in chunk_or_batch:
        return len(chunk_or_batch["energy"])
    else:
        # todo: make this more generic
        raise KeyError
