import numpy as np
import matplotlib.pyplot as plt
import climlab
from climlab import constants as const
import argparse
import json

def run_model(args, timestep):
    """
    Run the model with the given arguments.
    """
    # model creation
    ebm_model = climlab.EBM(name='My EBM', 
                            T0=float(args.t0), 
                            water_depth=float(args.water_depth),
                            timestep=timestep)

    # accessing the model time dictionary
    # ebm_model.time

    # print model parameters
    # ebm_model.param

    # print model states and suprocesses
    # print(ebm_model)

    # integrate model for two years
    ebm_model.integrate_years(1.)

    # integrate model until solution converges
    ebm_model.integrate_converge()

    # write results to netcdf
    results = ebm_model.to_xarray(diagnostics=True)
    results.to_netcdf('ebm_model_results.nc')

    return ebm_model

def generate_plot(ebm_model):

    # creating plot figure
    fig = plt.figure(figsize=(15,10))

    # Temperature plot
    ax1 = fig.add_subplot(221)
    ax1.plot(ebm_model.lat,ebm_model.Ts)

    ax1.set_xticks([-90,-60,-30,0,30,60,90])
    ax1.set_xlim([-90,90])
    ax1.set_title('Surface Temperature', fontsize=14)
    ax1.set_ylabel('(degC)', fontsize=12)
    ax1.grid()

    # Albedo plot
    ax2 = fig.add_subplot(223, sharex = ax1)
    ax2.plot(ebm_model.lat,ebm_model.albedo)

    ax2.set_title('Albedo', fontsize=14)
    ax2.set_xlabel('latitude', fontsize=10)
    ax2.set_ylim([0,1])
    ax2.grid()

    # Net Radiation plot
    ax3 = fig.add_subplot(222, sharex = ax1)
    ax3.plot(ebm_model.lat, ebm_model.OLR, label='OLR',
                                        color='cyan')
    ax3.plot(ebm_model.lat, ebm_model.ASR, label='ASR',
                                        color='magenta')
    ax3.plot(ebm_model.lat, ebm_model.ASR-ebm_model.OLR,
                                        label='net radiation',
                                        color='red')

    ax3.set_title('Net Radiation', fontsize=14)
    ax3.set_ylabel('(W/m$^2$)', fontsize=12)
    ax3.legend(loc='best')
    ax3.grid()

    # Energy Balance plot
    net_rad = np.squeeze(ebm_model.net_radiation)
    transport = np.squeeze(ebm_model.heat_transport_convergence)

    ax4 = fig.add_subplot(224, sharex = ax1)
    ax4.plot(ebm_model.lat, net_rad, label='net radiation',
                                                color='red')
    ax4.plot(ebm_model.lat, transport, label='heat transport',
                                                color='blue')
    ax4.plot(ebm_model.lat, net_rad+transport, label='balance',
                                                color='black')

    ax4.set_title('Energy', fontsize=14)
    ax4.set_xlabel('latitude', fontsize=10)
    ax4.set_ylabel('(W/m$^2$)', fontsize=12)
    ax4.legend(loc='best')
    ax4.grid()


    plt.savefig('ebm_results.png')

if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description='EBM Model')
    
    # have at least one argument
    parser.add_argument('--t0',
                        dest='t0',
                        default=12.0,
                        help='Initial temperature setting')
    parser.add_argument('--water_depth',
                        dest='water_depth',
                        default=10.0,
                        help='Depth of zonal mean surface domain, which the heat capacity is dependent on')                        
    args = parser.parse_args()
    with open('parameters.json', 'r') as f:
        params = json.loads(f.read())
    print(f"Running model with parameters\nT0: {args.t0}\nWater Depth: {args.water_depth}\nTimestep: {params['timestep']}\n")
    ebm_model = run_model(args, float(params['timestep']))
    generate_plot(ebm_model)