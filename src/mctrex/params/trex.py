"""
/*******************************************************************************
* T-Rex @ ESS
* Ver. 2026-09-02
*
* authors: Augustin Loesch, Lukas Bauer, Christian Franz
* Changes:
* 2024-10-28:	Removed phase_FAN variable
* 2025-01-21: 	Added slits after gaps to avoid rogue neutrons
*		        Added bender variable
* 2025-02-28:	Added honeycomb collimators (not correct parameters for now)
* 2026-01-23:   Removed all Fan related variables from code (MA)
* 2026-04-14:   Restricted RRM variable to certain values only fill all time frames
*               + Changed RRM  to int. (MA)
* 2026-05-12:   Changed MultiDisk to DiskChopper for the P- and M-choppers. (MA)
* 2026-07-24:   Added the aluminium windows from the Table of Optics (v3.0, CHESS 1535031).
*               PowderN with p_interact = 0.01. (MA)
* 2026-07-29:   Added CCR tails around the sample position (MA)
* 2026-07-30:   Added Radial Collimator to T-REX. Matching the drawings (MA)
* 2026-09-02:   Geometry compared against Table of Optics. Changed to Guide_gravity and
*               kept the 12km curvature radius. (MA)
* 2026-09-03:   NBOA asymmetric taper. The -x wall of sections 1-4 is FIXED at
*               -47.000 mm in the design OFF meshes; all horizontal narrowing
*               (90 -> 60 mm) is on the +x (cold moderator) wall. The guide
*               centre-line is therefore a straight line tilted by -0.213350 deg
*               = half the 0.426695 deg ToO horizontal taper angle, running from
*               -2.0295 mm at 1895.927 mm to -16.8711 mm at 5881.65 mm.
*               Sections 1-4 and Al_window_01 now hang off arm_NBOA; Guide_5
*               removes the tilt where the -x wall releases at 5.927 m.
*               L_Smon corrected to 163.170 m to follow the sample_monitor move
*               to the Guide_50a exit. (MA)
* 2026-09-05:   Curve rotations corrected on three counts (MA):
*                 (a) GAPS - each joint rotated by the preceding GUIDE length
*                     only, so 209.8 mm of arc (the 2-30 mm inter-section gaps)
*                     carried no rotation. Arms are now the true entrance-to-
*                     entrance path distance.
*                 (b) MIDPOINT RULE - each segment travelled its whole length at
*                     the angle it had at its START, while the true arc averages
*                     half a segment's turn more. Over 25 segments that cost
*                     sum(L^2)/2R = 13.7 mm of horizontal displacement. Each
*                     segment is now oriented at its own MIDPOINT angle:
*                     arm = d + (L_this - L_prev)/2, with Guide_5 carrying an
*                     extra L_5/2R at the curve entrance.
*                 (c) CLOSURE - the final joint (Guide_30) is set so the TOTAL
*                     bend is exactly (96.000-5.916)/12000 rad = 0.430119 deg,
*                     so the straight 67 m downstream leaves at the right angle.
*               Axis now tracks the OFF design model to under 1 mm over 163 m
*               (was 15.3 mm).
* 2026-09-04:   Added the 15 remaining aluminium windows, matching the July
*               OFF-file model (Al_window_02..14, 17, 18): same z positions,
*               thicknesses and apertures. Note July has no window at the ToO
*               41977/41998 pair, so neither does this file.
* 2026-09-08:   ALL 16 aluminium windows REMOVED for a like-for-like comparison
*               against the original OFF-file model, which has none. Al_window_01
*               is now an Arm so the arm_NBOA anchoring is untouched; the CCR
*               PowderN at the sample is unaffected. acc_power stays at 2 MW.
*               Also: f_M2 = f_M1, and the M-chopper nu values written longhand
*               (-f*RRM*0.5 and +f*RRM) so the pair counter-rotates. (MA)
*               All RELATIVE PREVIOUS references were first made explicit so
*               that inserting components cannot shift the chain; guide and
*               chopper positions verified unchanged to < 1 nm. (MA)
*
* N.B:  McStas manual mentions that the use of 'GROUP'/'WHEN'/'EXTEND' for the same component
*       leads to odd behavior. For that reason, only one DiskChopper is used, with the slit
*       size changing size, and two openings at 0/180. Delay in time can be analytically calculated
*       on the instrument IRL when swapping openings.
*******************************************************************************/
"""

from mctrex.params.choppers import bw1
from mctrex.params.guides_curve import guides_curve_1, guides_curve_2
from mctrex.params.guides_extraction import guides_extraction
from mctrex.params.source import ess_source

component_list = ess_source
component_list.extend(guides_extraction)
component_list.extend(guides_curve_1)
component_list.extend([bw1])
component_list.extend(guides_curve_2)

component_dict = {c.name: c for c in component_list}
