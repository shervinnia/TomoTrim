#!/bin/bash
#SBATCH --mem=100G
#SBATCH --output=name.out
#SBATCH -e errors.txt
#SBATCH -a 0-10000%100
#SBATCH -n 2
#SBATCH --export ALL

mpiexec -n 32 /software/RELION/latest4/bin/relion_tomo_subtomo_mpi --i ImportTomo/subtomocoords_trimmed/optimisation_set.star --t ImportTomo/WT5/tomograms.star --p ImportTomo/subtomocoords_trimmed/particles.star --o PseudoSubtomo/bin15box32_trimmed/ --b 32 --bin 15 --j 2


/software/RELION/latest4/bin/relion_refine --o InitialModel/bin15box32_trimmed/run --iter 100 --grad --denovo_3dref --i PseudoSubtomo/bin15box32_trimmed/particles.star --ctf --K 3 --sym C2 --flatten_solvent --zero_mask --dont_combine_weights_via_disc --pool 3 --pad 1 --skip_gridding --maxsig 5 --particle_diameter 750 --oversampling 1 --healpix_order 1 --offset_range 6 --offset_step 2 --auto_sampling --tau2_fudge 4 --gpu "0" && rm -f InitialModel/bin15box32_trimmed/RELION_JOB_EXIT_SUCCESS && /software/RELION/latest4/bin/relion_align_symmetry --i InitialModel/bin15box32_trimmed/run_it100_model.star --o InitialModel/bin5box32_trimmed/initial_model.mrc --sym C2 --apply_sym --select_largest_class && touch InitialModel/bin15box32_trimmed/RELION_JOB_EXIT_SUCCESS


mpiexec -n 3 /software/RELION/latest4/bin/relion_refine_mpi --o Refine3D/bin5box32_trimmed/run --auto_refine --split_random_halves --ios PseudoSubtomo/bin5box32_trimmed/optimisation_set.star --ref InitialModel/bin5box32_trimmed/initial_model.mrc --ini_high 60 --dont_combine_weights_via_disc --pool 3 --pad 2  --skip_gridding  --ctf --particle_diameter 200 --flatten_solvent --zero_mask --oversampling 1 --healpix_order 2 --auto_local_healpix_order 4 --offset_range 5 --offset_step 2 --sym C1 --low_resol_join_halves 40 --norm --scale  --j 1 --gpu ""
