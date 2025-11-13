## Concrete vs Abstract:

### Group: human
(human_map_pcc) T-statistic: -0.29234174075842534, P-value: 0.7707917492811607
(human_word_importance_pcc) T-statistic: 2.0427954463730185, P-value: 0.04440785998109138
(human_concatenate_pcc) T-statistic: -0.2916432269712574, P-value: 0.7713238607142109
### Group: grp1
(grp1_map_pcc) T-statistic: -0.34453442443020527, P-value: 0.7313599134451229
(grp1_word_importance_pcc) T-statistic: 1.7483758014458568, P-value: 0.08428370422420303
(grp1_concatenate_pcc) T-statistic: -0.3439439436824381, P-value: 0.7318022300107445
### Group: grp2
(grp2_map_pcc) T-statistic: -0.3818574778673187, P-value: 0.7035923133317876
(grp2_word_importance_pcc) T-statistic: 3.187056512484489, P-value: 0.0020594883117541173
(grp2_concatenate_pcc) T-statistic: -0.3808789136624779, P-value: 0.7043154200951909

## Grp1 vs Grp2:

(map_pcc) T-statistic: 8.882123821026486, P-value: 1.329872587405734e-15
(word_importance_pcc) T-statistic: 1.632851298949246, P-value: 0.10447903966793935
(concatenate_pcc) T-statistic: 8.880445952672957, P-value: 1.3433485040387226e-15


## Mixed-Effect Model Analysis for map_pcc:
                  Mixed Linear Model Regression Results
=========================================================================
Model:                   MixedLM       Dependent Variable:       map_pcc 
No. Observations:        320           Method:                   REML    
No. Groups:              160           Scale:                    0.0023  
Min. group size:         2             Log-Likelihood:           202.9625
Max. group size:         2             Converged:                Yes     
Mean group size:         2.0                                             
-------------------------------------------------------------------------
                               Coef.  Std.Err.   z    P>|z| [0.025 0.975]
-------------------------------------------------------------------------
Intercept                       0.287    0.026 11.130 0.000  0.237  0.338
group[T.grp2]                  -0.047    0.008 -6.202 0.000 -0.061 -0.032
condition[T.con]               -0.008    0.036 -0.212 0.832 -0.079  0.064
group[T.grp2]:condition[T.con] -0.001    0.011 -0.083 0.934 -0.022  0.020
trial_id Var                    0.051    0.175                           
=========================================================================



## Mixed-Effect Model Analysis for word_importance_pcc:
                  Mixed Linear Model Regression Results
=========================================================================
Model:                MixedLM   Dependent Variable:   word_importance_pcc
No. Observations:     320       Method:               REML               
No. Groups:           160       Scale:                0.0208             
Min. group size:      2         Log-Likelihood:       21.8386            
Max. group size:      2         Converged:            Yes                
Mean group size:      2.0                                                
-------------------------------------------------------------------------
                               Coef.  Std.Err.   z    P>|z| [0.025 0.975]
-------------------------------------------------------------------------
Intercept                       0.339    0.029 11.757 0.000  0.282  0.395
group[T.grp2]                  -0.054    0.023 -2.374 0.018 -0.099 -0.009
condition[T.con]                0.065    0.041  1.589 0.112 -0.015  0.145
group[T.grp2]:condition[T.con]  0.055    0.032  1.715 0.086 -0.008  0.118
trial_id Var                    0.046    0.062                           
=========================================================================



## Mixed-Effect Model Analysis for concatenate_pcc:
                  Mixed Linear Model Regression Results
=========================================================================
Model:                MixedLM     Dependent Variable:     concatenate_pcc
No. Observations:     320         Method:                 REML           
No. Groups:           160         Scale:                  0.0023         
Min. group size:      2           Log-Likelihood:         203.0296       
Max. group size:      2           Converged:              Yes            
Mean group size:      2.0                                                
-------------------------------------------------------------------------
                               Coef.  Std.Err.   z    P>|z| [0.025 0.975]
-------------------------------------------------------------------------
Intercept                       0.287    0.026 11.133 0.000  0.237  0.338
group[T.grp2]                  -0.047    0.008 -6.202 0.000 -0.061 -0.032
condition[T.con]               -0.008    0.036 -0.212 0.832 -0.079  0.064
group[T.grp2]:condition[T.con] -0.001    0.011 -0.082 0.935 -0.022  0.020
trial_id Var                    0.051    0.175                           
=========================================================================