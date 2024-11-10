import sys
import ast
import datetime
import numpy as np
from sqlalchemy import null

import utilities
from models import postgres_session
# Import the necessary models
from models.archery import Shots, Ends, Rounds


class Round:
    def __init__(
        self, round_date_, range_id_, distance_m_, target_id_, sight_, clicker_, stabilisation_, riser_id_, limb_id_,
        score_list_, hunger_, start_time=None, end_time=None, draw_weight_lb_=None, arrow_id_=None,
        condition_mental=None, condition_env=None
    ):
        # direct data
        self.round_date = round_date_
        self.range_id = range_id_
        self.distance_m = distance_m_
        self.target_id = target_id_
        self.sight = sight_
        self.clicker = clicker_
        self.stabilisation = stabilisation_
        self.riser_id = riser_id_
        self.limb_id = limb_id_
        self.score_list = score_list_
        self.hunger = hunger_
        self.start_time = start_time
        self.end_time = end_time
        self.draw_weight_lb = draw_weight_lb_
        self.arrow_id = arrow_id_
        self.conditional_mental = condition_mental
        self.conditional_env = condition_env

        # derived data
        self.round_obj = None
        self.round_id = None
        self.end_num_shots = []
        self.end_scores = []
        self.shots_scores = []
        self.shots_scores_actual = []  # convert x into 10
        self.ends = []  # list of dicts for db insert
        self.shots = []  # list of dicts for db insert
        self.num_x = 0
        self.num_10 = 0
        self.num_9 = 0
        self.total_score = 0
        self.stdev_ends = None
        self.stdev_shots = None
        self.avg_shots = None
        self.num_ends = 0
        self.num_shots = 0
        self.days_since_last = None

    def construct_round(self, db_session):
        end_obj_list = []
        for i, end_list in enumerate(self.score_list):
            shots_list = []
            end_total = 0
            end_num_shots = 0
            for j, score in enumerate(end_list):
                if isinstance(score, str) and score.lower() == 'x':
                    self.num_x += 1
                    self.shots_scores_actual.append(10)
                    self.shots_scores.append(score)
                    end_num_shots += 1
                    self.num_shots += 1
                    end_total += 10
                    shots_list.append(Shots(shot=j + 1, score=10, is_x=True))
                    continue
                if score == 10:
                    self.num_10 += 1
                elif score == 9:
                    self.num_9 += 1
                self.num_shots += 1
                self.shots_scores.append(score)
                end_total += score
                end_num_shots += 1
                self.shots_scores_actual.append(score)
                shots_list.append(Shots(shot=j + 1, score=score, is_x=False))
            end_obj_list.append(Ends(
                end=i + 1, score_total=end_total, num_shots=end_num_shots, shots_ordered=True, archery_shot=shots_list
            ))
            self.num_ends += 1
            self.end_scores.append(end_total)
            self.end_num_shots.append(end_num_shots)
            self.total_score += end_total

        self.stdev_ends = np.std(self.end_scores)
        self.stdev_shots = np.std(self.shots_scores_actual)
        self.avg_shots = np.mean(self.shots_scores_actual)
        self.days_since_last = self.get_days_since_last(db_session)
        self.round_obj = Rounds(
            date=self.round_date, archery_range_id=self.range_id, distance_m=self.distance_m,
            archery_target_id=self.target_id, sight=self.sight, clicker=self.clicker, stabilisation=self.stabilisation,
            archery_riser_id=self.riser_id, archery_limb_id=self.limb_id, draw_weight_lb=self.draw_weight_lb,
            archery_arrow_id=self.arrow_id, total_score=self.total_score, num_x=self.num_x, num_10=self.num_10,
            num_9=self.num_9, stdev_ends=self.stdev_ends, stdev_shots=self.stdev_shots, avg_shots=self.avg_shots,
            num_ends=self.num_ends, num_shots=self.num_shots, condition_mental=self.conditional_mental,
            condition_env=self.conditional_env, hunger=self.hunger,
            start_time=self.start_time if self.start_time else null(),
            end_time=self.end_time if self.end_time else null(),
            days_since_last_practice=self.days_since_last,
            ends=end_obj_list,
        )

    def get_days_since_last(self, db_session):
        q_stmt = 'select max(date) from archery_round'
        q_result = utilities.execute_any_q_text(db_session.bind, q_stmt)
        if len(q_result) > 0:
            date_previous = q_result[0][0]
        else:
            return
        return (self.round_date.date() - date_previous).days

    def insert_round(self, db_session):
        db_session.add(self.round_obj)
        print('committing...')
        db_session.commit()


def insert_archery_round(
    db_session, round_date_, range_id_, distance_m_, target_id_, sight_, clicker_, stabilisation_, riser_id_, limb_id_,
    score_list, hunger_, start_time=None, end_time=None, draw_weight_lb_=None, arrow_id_=None, condition_mental=None,
    condition_env=None
):
    round_obj = Round(
        round_date_, range_id_, distance_m_, target_id_, sight_, clicker_, stabilisation_, riser_id_, limb_id_,
        score_list, hunger_, start_time=start_time, end_time=end_time, draw_weight_lb_=draw_weight_lb_,
        arrow_id_=arrow_id_, condition_mental=condition_mental, condition_env=condition_env
    )
    round_obj.construct_round(db_session)
    round_obj.insert_round(db_session)


if __name__ == '__main__':
    riser_id = int(sys.argv[1])
    limb_id = int(sys.argv[2])
    range_id = int(sys.argv[3])
    arrow_id = int(sys.argv[4])
    target_id = int(sys.argv[5])
    distance_m = float(sys.argv[6])
    sight = ast.literal_eval(sys.argv[7])
    stabilisation = ast.literal_eval(sys.argv[8])
    clicker = ast.literal_eval(sys.argv[9])
    draw_weight_lb = float(sys.argv[10])
    env_mental = int(sys.argv[11])
    env_physical = int(sys.argv[12])
    hunger = ast.literal_eval(sys.argv[13])
    start_hhmm = sys.argv[14]
    end_hhmm = sys.argv[15]
    scores_string = sys.argv[16]
    round_date_str = sys.argv[17]
    round_date = datetime.datetime.strptime(round_date_str, '%Y%m%d')

    # Convert the input string to a Python list of lists
    scores_list = ast.literal_eval(scores_string)

    # # TEST
    # riser_id = 1
    # limb_id = 1
    # range_id = 1
    # arrow_id = 1
    # target_id = 1
    # distance_m = 1
    # sight = True
    # stabilisation = False
    # clicker = False
    # draw_weight_lb = 26
    # env_mental = 8
    # env_physical = 10
    # hunger = False
    # start_hhmm = '1400'
    # end_hhmm = '1430'
    # round_date_str = '20241103'
    # round_date = datetime.datetime.strptime(round_date_str, '%Y%m%d')
    #
    # # Convert the input string to a Python list of lists
    # scores_list = [[1, 2, 3, 4], [4, 'x', 2, 1]]
    # # TEST END

    insert_archery_round(
        postgres_session, round_date, range_id, distance_m, target_id, sight, clicker, stabilisation, riser_id, limb_id,
        scores_list, hunger, start_time=start_hhmm, end_time=end_hhmm, draw_weight_lb_=draw_weight_lb,
        arrow_id_=arrow_id, condition_mental=env_mental, condition_env=env_physical
    )
