import os
import pandas as pd
import urbansim.sim.simulation as sim
from activitysim import activitysim as asim
from .util.vectorize_tour_scheduling import vectorize_tour_scheduling

"""
This model predicts the departure time and duration of each activity for
mandatory tours
"""


@sim.table()
def tdd_alts(configs_dir):
    # right now this file just contains the start and end hour
    f = os.path.join(configs_dir, "configs",
                     "tour_departure_and_duration_alternatives.csv")
    return pd.read_csv(f)


# used to have duration in the actual alternative csv file,
# but this is probably better as a computed column like this
@sim.column("tdd_alts")
def duration(tdd_alts):
    return tdd_alts.end - tdd_alts.start


@sim.table()
def tdd_work_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs',
                     'tour_departure_and_duration_work.csv')
    return asim.read_model_spec(f).fillna(0)


@sim.model()
def work_scheduling(set_random_seed,
                    mandatory_tours_merged,
                    tdd_alts,
                    tdd_work_spec):

    tours = mandatory_tours_merged.to_frame()
    alts = tdd_alts.to_frame()
    spec = tdd_work_spec.to_frame()

    tours = tours[tours.tour_type == "work"]

    print "Running %d work tour scheduling choices" % len(tours)

    choices = vectorize_tour_scheduling(tours, alts, spec)

    print "Choices:\n", choices.describe()

    sim.add_column("mandatory_tours",
                   "tour_departure_and_duration",
                   choices)


@sim.table()
def tdd_school_spec(configs_dir):
    f = os.path.join(configs_dir, 'configs',
                     'tour_departure_and_duration_school.csv')
    return asim.read_model_spec(f).fillna(0)


@sim.model()
def school_scheduling(set_random_seed,
                      mandatory_tours_merged,
                      tdd_alts,
                      tdd_school_spec):

    tours = mandatory_tours_merged.to_frame()
    alts = tdd_alts.to_frame()
    spec = tdd_school_spec.to_frame()

    tours = tours[tours.tour_type == "school"]

    print "Running %d school tour scheduling choices" % len(tours)

    choices = vectorize_tour_scheduling(tours, alts, spec)

    print "Choices:\n", choices.describe()

    sim.add_column("mandatory_tours",
                   "tour_departure_and_duration",
                   choices)
