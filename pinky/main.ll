; ModuleID = "pinky_subset"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
.2:
  %".3" = sub double              0x0, 0x4014000000000000
  %".4" = fmul double 0x4012666666666666, %".3"
  %".5" = fadd double 0x4059000000000000, %".4"
  %".6" = sub double              0x0, 0x4000000000000000
  %".7" = fsub double %".5", %".6"
  %".8" = fdiv double 0x4003333333333333, 0x4000000000000000
  %".9" = fadd double %".7", %".8"
}
