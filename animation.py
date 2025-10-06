import os
import pyvista as pv
from glob import glob
import time


def animate_velocity(geoFn, interp_planes, save=False):
    """
    Animate inlet velocity arrows on the inlet plane

    Args:
        - geoFn: Path to the aortic geometry
        - interp_planes: list of pv objects corresponds to the inlet planes with vectorial velocity data
        - save: bool flag for saving scenes

    Return: None
    """
    
    num_frames = len(interp_planes);

    geo = pv.read(geoFn);
    plotter = pv.Plotter();
    plotter.add_mesh(geo, opacity=.3);
    plotter.show_axes();
    
    p = interp_planes[0];
    pp = p.extract_points(range(0, p.n_points, 10));
    arr = pp.glyph(orient="Velocity",
                scale=False,
                factor=.02
                );
    
    actor = plotter.add_text(
            f'Time pt: 1 out of {num_frames}',
            position='upper_right',
            color='blue',
            shadow=True,
            font_size=16,
        );

    plane_actor = plotter.add_mesh(pp, 
                                   color='lightgrey', 
                                   opacity=1);
    arrow_actor = plotter.add_mesh(arr, 
                                   scalar_bar_args={'title': 'Velocity Magnitude'},
                                   cmap='jet');
    
    if save:
        os.makedirs('./scene', exist_ok=True);
        plotter.save_graphic(os.path.join("./scene", f"img1.svg"));

    plotter.show(auto_close=False, interactive_update=True);

    for i in range(1, num_frames):
        p = interp_planes[i];
        pp = p.extract_points(range(0, p.n_points, 10));
        arr = pp.glyph(orient="Velocity",scale=False,factor=.02);

        # update existing actors instead of re-adding
        plane_actor.mapper.SetInputData(pp);
        arrow_actor.mapper.SetInputData(arr);
        actor.set_text('upper_right', f'Time pt: {i+1}/{num_frames}');
        plotter.update();

        if save:
            plotter.save_graphic(os.path.join("./scene", f"img{i+1}.svg"));

        time.sleep(1);  # pause between frames


def main():
    profilesDir = r'G:\ZhongShan_Data\ZS-ASAD03\pre_MR_processed\mapped_result'
    geoFn = r'G:\ZhongShan_Data\ZS-ASAD03\ZS03_pre_aligned_smoothed.stl'

    interp_planes = [pv.read(fn) for fn in sorted(glob(os.path.join(profilesDir, '*.vtp')))]
    animate_velocity(geoFn, interp_planes)

if __name__=="__main__":
    main()