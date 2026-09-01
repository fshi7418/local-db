"""Canonical skeet target sequences and a builder for shot-by-shot rows.

A target is a 4-tuple of (station, house, single_double, pair_order), where
pair_order is 1 or 2 within a double and None for a single.
"""
from models.firearm import SkeetShot


# the only values skeet_shot.house takes; import these wherever it is validated
HIGH = 'high'
LOW = 'low'
HOUSES = (HIGH, LOW)

# likewise for skeet_shot.single_double
SINGLE = 'single'
DOUBLE = 'double'
SINGLE_DOUBLES = (SINGLE, DOUBLE)

INTERNATIONAL = [
    (1, HIGH, SINGLE, None), (1, HIGH, DOUBLE, 1), (1, LOW, DOUBLE, 2),
    (2, HIGH, SINGLE, None), (2, HIGH, DOUBLE, 1), (2, LOW, DOUBLE, 2),
    (3, HIGH, SINGLE, None), (3, HIGH, DOUBLE, 1), (3, LOW, DOUBLE, 2),
    (4, HIGH, SINGLE, None), (4, LOW, SINGLE, None),
    (5, LOW, SINGLE, None), (5, LOW, DOUBLE, 1), (5, HIGH, DOUBLE, 2),
    (6, LOW, SINGLE, None), (6, LOW, DOUBLE, 1), (6, HIGH, DOUBLE, 2),
    (7, LOW, DOUBLE, 1), (7, HIGH, DOUBLE, 2),
    (4, HIGH, DOUBLE, 1), (4, LOW, DOUBLE, 2),
    (4, LOW, DOUBLE, 1), (4, HIGH, DOUBLE, 2),
    (8, HIGH, SINGLE, None), (8, LOW, SINGLE, None),
]

AMERICAN = [
    (1, HIGH, SINGLE, None), (1, LOW, SINGLE, None), (1, HIGH, DOUBLE, 1), (1, LOW, DOUBLE, 2),
    (2, HIGH, SINGLE, None), (2, LOW, SINGLE, None), (2, HIGH, DOUBLE, 1), (2, LOW, DOUBLE, 2),
    (3, HIGH, SINGLE, None), (3, LOW, SINGLE, None),
    (4, HIGH, SINGLE, None), (4, LOW, SINGLE, None),
    (5, HIGH, SINGLE, None), (5, LOW, SINGLE, None),
    (6, HIGH, SINGLE, None), (6, LOW, SINGLE, None), (6, LOW, DOUBLE, 1), (6, HIGH, DOUBLE, 2),
    (7, HIGH, SINGLE, None), (7, LOW, SINGLE, None), (7, LOW, DOUBLE, 1), (7, HIGH, DOUBLE, 2),
    (8, HIGH, SINGLE, None), (8, LOW, SINGLE, None),
]

SEQUENCES = {
    'International': INTERNATIONAL,
    'American': AMERICAN,
}


def build_skeet_shots(discipline, breaks, skeet_round_id=None):
    """Turn a list of hit/miss booleans into SkeetShot rows.

    `breaks` is in the order the shots were fired: 25 entries either way. Each
    row gets a `shot_order` (1..25, the order fired) and a `target_number` (the
    target's position in the sequence above, 1..25 international / 1..24
    American). The two only diverge for American skeet, where the option shot
    repeats the `target_number` it makes up and shifts everything after it.
    """
    sequence = SEQUENCES.get(discipline)
    if sequence is None:
        raise ValueError(f'unknown skeet discipline: {discipline}')
    breaks = [bool(b) for b in breaks]
    expected = len(sequence) if discipline != 'American' else len(sequence) + 1
    if len(breaks) != expected:
        raise ValueError(f'{discipline} skeet takes {expected} shots, got {len(breaks)}')

    shots = []
    option_used = discipline != 'American'
    missed = None  # the target the option will repeat, once one is missed
    cursor = 0  # how far into the sequence we are, 0-based
    for shot_order, broken in enumerate(breaks, start=1):
        # the option is taken as soon as a miss has happened and any double in
        # progress has been completed; a clean first 24 pushes it to shot 25,
        # where it repeats the last target of the sequence (station 8 low house)
        mid_double = bool(shots) and shots[-1].single_double == DOUBLE and shots[-1].pair_order == 1
        exhausted = cursor >= len(sequence)
        if not option_used and not mid_double and (missed is not None or exhausted):
            repeated = missed if missed is not None else shots[-1]
            option_used = True
            shots.append(SkeetShot(
                skeet_round_id=skeet_round_id,
                shot_order=shot_order,
                target_number=repeated.target_number,
                station=repeated.station,
                house=repeated.house,
                single_double=SINGLE,
                pair_order=None,
                is_option=True,
                broken=broken,
            ))
            continue

        if exhausted:
            raise ValueError(f'shot {shot_order} runs past the end of the sequence')
        station, house, single_double, pair_order = sequence[cursor]
        cursor += 1
        shot = SkeetShot(
            skeet_round_id=skeet_round_id,
            shot_order=shot_order,
            target_number=cursor,
            station=station,
            house=house,
            single_double=single_double,
            pair_order=pair_order,
            is_option=False,
            broken=broken,
        )
        shots.append(shot)
        if missed is None and not broken:
            missed = shot

    if cursor != len(sequence) or not option_used:
        raise ValueError(f'{discipline} shot list does not cover the full sequence')
    return shots
