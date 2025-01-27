import vapoursynth as vs
core = vs.core
import functools
import math

# auto white from http://www.vapoursynth.com/doc/functions/frameeval.html
def AutoWhiteAdjust(n, f, clip, core):
   small_number = 0.000000001
   red   = f[0].props['PlaneStatsAverage']
   green = f[1].props['PlaneStatsAverage']
   blue  = f[2].props['PlaneStatsAverage']
   max_rgb = max(red, green, blue)
   red_corr   = max_rgb/max(red, small_number)
   green_corr = max_rgb/max(green, small_number)
   blue_corr  = max_rgb/max(blue, small_number)
   norm = max(blue, math.sqrt(red_corr*red_corr + green_corr*green_corr + blue_corr*blue_corr) / math.sqrt(3), small_number)
   r_gain = red_corr/norm
   g_gain = green_corr/norm
   b_gain = blue_corr/norm
   return core.std.Expr(clip, expr=['x ' + repr(r_gain) + ' *', 'x ' + repr(g_gain) + ' *', 'x ' + repr(b_gain) + ' *'])

def AutoWhite(clip):
   rgb_clip = clip
   r_avg = core.std.PlaneStats(rgb_clip, plane=0)
   g_avg = core.std.PlaneStats(rgb_clip, plane=1)
   b_avg = core.std.PlaneStats(rgb_clip, plane=2)
   return core.std.FrameEval(rgb_clip, functools.partial(AutoWhiteAdjust, clip=rgb_clip, core=core), prop_src=[r_avg, g_avg, b_avg])
   
