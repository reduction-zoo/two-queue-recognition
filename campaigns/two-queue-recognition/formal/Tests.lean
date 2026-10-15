import Challenge
open TwoQueueRecognition
example : sourceWitness ⟨4,[(0,3),(1,2)]⟩ [0,1,2,3] = false := by native_decide
example : targetWitness ⟨4,[(0,3),(1,2)]⟩ ([0,1,2,3],[false,true]) = true := by native_decide
