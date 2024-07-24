# """Add entries for new WAV files."""
#
# import logging
# from collections.abc import Collection
#
# from ...model.chk.wav.wav_constants import MAX_WAV_FILES
# from ...model.richchk.swnm.rich_switch import RichSwitch
# from ...model.richchk.swnm.rich_swnm_section import RichSwnmSection
# from ...model.richchk.wav.rich_wav_section import RichWavSection
# from ...util import logger
#
#
# class RichWavEditor:
#     def __init__(self) -> None:
#         self.log: logging.Logger = logger.get_logger(RichWavEditor.__name__)
#
#     def add_wavs_files(
#         self, switches: Collection[RichSwitch], wav: RichWavSection
#     ) -> RichWavSection:
#         """Add the switches to the SWNM, allocating switch IDs where appropriate."""
#         unique_switches_to_add = self._build_switches_set(switches)
#         allocable_ids = self._generate_allocable_ids(wav)
#         new_switches = [x for x in wav.wavs]
#         for i, switch in enumerate(unique_switches_to_add):
#             if not allocable_ids:
#                 msg = (
#                     f"No more allocable IDs left.  Have we run out of switches?  "
#                     f"{i + 1} remaining switches we cannot allocate."
#                 )
#                 self.log.error(msg)
#                 raise ValueError(msg)
#             if switch.index is not None:
#                 if switch not in new_switches:
#                     new_switches[switch.index] = switch
#                     if switch.index in allocable_ids:
#                         allocable_ids.remove(switch.index)
#                 else:
#                     self.log.warning(
#                         f"Attempted to add a switch to the SWNM whose ID {switch.index} "
#                         f"is already allocated.  "
#                         f"Not replacing.  "
#                     )
#             else:
#                 new_switches.append(
#                     RichSwitch(
#                         _custom_name=switch.custom_name, _index=allocable_ids.pop()
#                     )
#                 )
#         return RichSwnmSection(_switches=new_switches)
#
#     def _build_switches_set(self, switches: Collection[RichSwitch]) -> set[RichSwitch]:
#         unique_switches = set(switches)
#         if len(switches) < len(switches):
#             num_duplicates = len(switches) - len(unique_switches)
#             self.log.warning(
#                 f"There are {num_duplicates} duplicate switches.  "
#                 f"Only one of each unique location is allocated to the SWNM."
#             )
#         return set(switches)
#
#     @classmethod
#     def _generate_allocable_ids(cls, wav: RichWavSection) -> list[int]:
#         """Generate all available ids when adding a new wav file to the WAV."""
#         possible_ids = range(0, MAX_WAV_FILES)
#         already_used_ids = [x.index for x in wav.wavs]
#         allocable_ids = [
#             index for index in possible_ids if index not in already_used_ids
#         ]
#         # pop from smallest index to largest
#         allocable_ids.reverse()
#         return allocable_ids
