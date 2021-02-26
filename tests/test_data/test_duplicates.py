from data.src.languages_update import _remove_mismatch_ids, _get_alias

def _remove_duplicates(script_dict: Dict[str, str]) -> Dict[str, str]:
    """If a values in lang["script"] appears more than once, the [key:value] pair that does not conform to ISO unicode
    entries returned from unicodedataplus.property_value_aliases["script"] the key is deleted.
    """
    remove = []
    for key, value in script_dict["script"].items():
        value = value.replace(" ", "_")
        if _get_alias(value) != key:
            remove.append(key)
    for i in remove:
        del script_dict["script"][i]
    return script_dict