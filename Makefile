# Makefile for source rpm: gdm
# $Id$
NAME := gdm
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
