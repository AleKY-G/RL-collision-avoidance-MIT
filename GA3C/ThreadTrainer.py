# Copyright (c) 2016, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
from threading import Thread
from Config import GA3CConfig; Config = GA3CConfig()


class ThreadTrainer(Thread):
    def __init__(self, server, id):
        super(ThreadTrainer, self).__init__()
        self.setDaemon(True)
        self.id        = id
        self.server    = server
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            batch_size = 0

            while batch_size <= Config.TRAINING_MIN_BATCH_SIZE:
                if Config.GAME_CHOICE == Config.game_collision_avoidance:
                    agent_states_, r_, a_ = self.server.training_q.get()
                    if batch_size == 0:
                        agent_states__ = agent_states_; r__ = r_; a__ = a_
                    else:
                        agent_states__ = np.concatenate((agent_states__, agent_states_))
                        r__ = np.concatenate((r__, r_))
                        a__ = np.concatenate((a__, a_))
                    batch_size += agent_states_.shape[0]

                else:

                    image_, r_, a_ = self.server.training_q.get()
                    
                    if batch_size == 0:
                        image__ = image_; r__ = r_; a__ = a_
                    else:
                        image__ = np.concatenate((image__, image_))
                        r__ = np.concatenate((r__, r_))
                        a__ = np.concatenate((a__, a_))
                    batch_size += image_.shape[0]
            
            if Config.TRAIN_MODE:
                if Config.GAME_CHOICE == Config.game_collision_avoidance:
                    # self.server.train_model(agent_states__[:,0,:], None, r__, a__, self.id)
                    self.server.train_model(agent_states__, r__, a__, self.id)
                else:
                    self.server.train_model(image__, r__, a__, self.id)
