#!/home/qcr/anaconda3/envs/rdk-env/bin/python
# coding: utf-8

from opentrons import protocol_api
metadata = {'apiLevel': '2.0'}

def run(protocol: protocol_api.ProtocolContext):

	# add 100 uL quench to all the wells
	# mix before, transfer XXX to LC plate
	# transfer 600 - XXX of MeCN to LC plate

	quench_vol = 100
	quenched_transfer_vol = 40
	# pipettes and tipracks
	tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul',1)
	tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul',4)

	p300_m = protocol.load_instrument('p300_multi', 'right', tip_racks=[tiprack_1,tiprack_2])

	# trough holding quench and MeCN solution
	trough = protocol.load_labware('custom_1x2_trough', 6)

	# reaction setup plate
	rxn_plate = protocol.load_labware('custom_12x8_reaction_plate',3)
	LC_plate = protocol.load_labware("custom_12x8_quench_plate",2)

	p300_m.well_bottom_clearance.dispense = 20
	# lowered aspirate height since we're using the trough
	p300_m.well_bottom_clearance.aspirate = 3
	p300_m.flow_rate.aspirate = 75
	p300_m.flow_rate.dispense = 200


	# if False, return tip to tiprack
	trash = True

	#alternately uncomment the 2 blocks below to run 1 block at a time

	# # add 100 uL quench to all the wells
	print("transferring quench from trough to reactor plate")

	p300_m.transfer(quench_vol,
	trough['A1'],
	rxn_plate.rows_by_name()['A'],
	new_tip='once', air_gap=10,trash=trash)
	#
	protocol.pause("quench transfer done")

	# mix before, transfer XXX to LC plate

	p300_m.transfer(quenched_transfer_vol,
	rxn_plate.rows_by_name()['A'],
	LC_plate.rows_by_name()['A'],
	# [dest.wells_by_name()[i] for i in ["A1","E1"]],
	new_tip="always",blow_out_location="source well",mix_before = (3,100),trash=trash)


	# transfer 600 - XXX of MeCN to LC plate


	p300_m.transfer(600-quenched_transfer_vol,
	trough['A2'],
	LC_plate.rows_by_name()['A'],
	# [dest.wells_by_name()[i] for i in ["A1","E1"]],
	new_tip="once",blow_out_location="source well",trash=trash)
