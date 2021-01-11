import numpy as np
import time

def make_nanmask(r,  ca):
    for i in range(len(r)):
        for j in range(len(r)):
            if r[i][j] <= ca:
                r[i][j] = 1
            else:
                r[i][j] = 0
    return r

def fft_BPM(E, P, lamb, Xmax, Ymax, delta_z, delta_x, Z, n0):
    Nx, Ny = np.shape(E)
    Nz = Z/delta_z

    delta_f = 1/(Nx*delta_x)
    # P = propagator(lamb, Nx, Ny, Xmax, delta_x, delta_z, n0)
    Eout = E
    for i in range(int(Nz)):
        Eout = ft2(Eout, delta_x)
        Eout = P * Eout
        Eout = ift2(Eout, delta_f)
    return Eout

def propagator(lamb, Nx, Ny, Xmax, delta_x, delta_z, n0):
    P = np.zeros((Nx, Ny), dtype=complex)
    k0 = 2*np.pi/lamb
    k02 = np.power(k0, 2)
    ky2 = []
    kx2 = []
    for i in range(Ny):
        ky = (2*np.pi / (2*Xmax*n0)) * (i-Ny/2)
        ky2.append(np.power(ky, 2))
        kx = (2 * np.pi / (2*Xmax*n0)) * (i - Nx / 2)
        kx2.append(np.power(kx, 2))

    for i in range(Ny):
        for j in range(Nx):
            P[j][i] = np.exp(complex("-j") * delta_z * (n0 * np.sqrt(k02 - kx2[j] - ky2[i]) - k0*n0))
    return P

def ft2(g, delta):
    G = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(g))) * np.power(delta, 2)
    return G

def ift2(g, delta):
    N = len(g)
    G = np.fft.ifftshift(np.fft.ifft2(np.fft.ifftshift(g))) * np.power(N * delta, 2)
    return G

def ft_phase_screen(r0, N, delta, L0, l0):
    # Set PSD
    del_f = 1/(N*delta)
    fx = []
    tmp = []
    for i in range(512):
        tmp.append(-256 + i)
    for i in range(512):
        fx.append(tmp)
    fx = np.array(fx)
    # frequency grid [1/m]
    fy = np.transpose(fx)
    f, th = cart2pol(fx, fy)
    fm = 5.92/l0/(2*np.pi)
    f0 = 1/L0
    # modified von Karman atmospheric phase PSD
    PSD_phi = 0.023*np.power(r0, -5/3) * np.exp(-np.power((f/fm), 2))/ np.power((np.power(f, 2) + np.power(f0, 2)), 11/6)
    PSD_phi[256][256] = 0
    # random draws of Fourier coefficients
    A = np.random.randn(N, N)
    B = np.random.randn(N, N)

    cn = (A + complex("j")*B) * np.sqrt(PSD_phi)*del_f
    phz = np.real(ift2(cn,1))
    return phz

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def lens_against_ft(Uin, wvl, d1, f):
    N = len(Uin[:,0])
    k = 2 * np.pi / wvl
    fx = []
    x2 = []
    y2 = []
    for i in range(512):
        fx.append((-256 + i) * wvl * f)
    for i in range(512):
        x2.append(fx)
    y2 = np.transpose(x2)
    Uout = np.exp(complex("j") * k / (2*f) * (np.power(x2, 2) + np.power(y2, 2))) / (complex("j")*wvl*f) * ft2(Uin, d1)
    return Uout, np.array(x2), np.array(y2)

def dm():
    n_pixels = 512
    n_act = 9
    coupling = 0.2
    Gaussian_idx = 2
    infl_amp = 5e-7
    n_act = 9

    x = np.linspace(-1, 1, n_pixels)
    y = np.linspace(-1, 1, n_pixels)
    X, Y = np.meshgrid(x, y)
    a_x = np.linspace(-1, 1, n_act)
    a_y = np.linspace(-1, 1, n_act)

    a_idx = np.linspace(1, n_act ** 2, n_act ** 2, axis=-1).reshape((n_act ** 2, 1))

    infl = np.zeros((512, 512, n_act ** 2))
    d_s = (np.max(a_x)-np.min(a_x))/ n_act
    for j in range(n_act):
        for i in range(n_act):
            r = np.sqrt(np.power(X - a_x[i], 2) + np.power(Y - a_y[j], 2))
            z = np.exp(np.log(coupling) * np.power(r / d_s, Gaussian_idx))
            infl[:, :, j * n_act + i] = z * infl_amp

    infl_t = infl.reshape(n_pixels ** 2, len(a_idx))
    invs = np.linalg.pinv(infl_t)
    return infl_t, invs