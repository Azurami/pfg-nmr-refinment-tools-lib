<h1> A tool to process and refine PFG NMR pseudo 2D spectra </h1>
<h1> About </h1>
Python library to process PFG NMR pseudo 2D spectra.

<h1> Usage </h1>

You should provide the following inputs: gamma (Hz/G), gradient pulse duration (s), diffusion time (s), the right point of region for integration (in points), the left point of region for integration (in points), relative path to spectra directory without spaces (the number of 1D spectra in aascii fromat with 'ascii-spec.txt' filename, see sample_data), relative path to difflist without spaces (gradients in G/cm). The left point should be less than the right one.

You can test the tool on sample data by following command:
<div class="highlight highlight-source-shell"><pre>
python process.py -gamma=4258.0 -small_delta=0.0054 -big_delta=0.1 -left_point=1000 -right_point=19000 -specdir=\sample_data\spectra -difflist=\sample_data\difflist -resultsdir=\results

</div>

General execution command:
<div class="highlight highlight-source-shell"><pre>
usage: process.py -gamma GAMMA] [-small_delta SMALL_DELTA] [-big_delta BIG_DELTA] [-left_point LEFT_POINT] [-right_point RIGHT_POINT] [-specdir SPECDIR]
                  [-difflist DIFFLIST] [-resultsdir RESULTSDIR]

</div>



