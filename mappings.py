from analysers import accuracy, corr, mean_std, shape, f1, mse, r2, mae
import pages.sections.accuracy as accuracy_sec
import pages.sections.corr as corr_sec
import pages.sections.mean_std as mean_std_sec
import pages.sections.shape as shape_sec
import pages.sections.f1 as f1_sec
import pages.sections.mse as mse_sec
import pages.sections.r2 as r2_sec
import pages.sections.mae as mae_sec


def analyser_to_section(analyst):
    if isinstance(analyst, accuracy.AccuracyAnalyser):
        return accuracy_sec.AccuracySection()
    elif isinstance(analyst, corr.CorrAnalyser):
        return corr_sec.CorrSection()
    elif isinstance(analyst, mean_std.MeanStdAnalyser):
        return mean_std_sec.MeanStdSection()
    elif isinstance(analyst, shape.ShapeAnalyser):
        return shape_sec.ShapeSection()
    elif isinstance(analyst, f1.F1Analyser):
        return f1_sec.F1Section()
    elif isinstance(analyst, mse.MSEAnalyser):
        return mse_sec.MSESection()
    elif isinstance(analyst, r2.R2Analyser):
        return r2_sec.R2Section()
    elif isinstance(analyst, mae.MAEAnalyser):
        return mae_sec.MAESection()
    else:
        raise ValueError('Unknown type found.')
