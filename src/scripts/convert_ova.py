import subprocess
import typer
from main import app

@app.command()
def vagrant(vmid: str, boxname: str):
    """
    Convertit une machine virtuelle en une boîte Vagrant.
    """
    # Affiche la liste des machines virtuelles
    typer.echo("Liste des machines virtuelles :")
    typer.run("VBoxManage list vms")

    # Crée la box Vagrant
    typer.echo("Création de la box Vagrant en cours, veuillez patienter...")
    typer.run(f"vagrant package --base {vmid} --output {boxname}.box")

    # Ajoute la nouvelle box à la liste des box Vagrant locales
    typer.echo("Ajout de la nouvelle box à la liste des box Vagrant locales :")
    typer.run(f"vagrant box add {boxname} {boxname}.box")

    # Initialise, démarre et se connecte à la nouvelle box
    typer.echo("Initialisation de la nouvelle box :")
    typer.run(f"vagrant init {boxname}")
    typer.echo("Démarrage de la nouvelle box :")
    typer.run("vagrant up")
    typer.echo("Connexion à la nouvelle box :")
    typer.run("vagrant ssh")
    typer.echo("Enjoy!")

@app.command()
def docker(image: str, nom_image: str):
    """Cette commande permet de convertir une image OVA en une image Docker."""

    # Extraction de l'archive OVA pour récupérer l'image de disque VMDK
    subprocess.run(['tar', '-xvf', f'{image}.ova'])
    # Conversion de l'image VMDK en format brut
    subprocess.run(['qemu-img', 'convert', '-f', 'vmdk', f'{image}.vmdk', '-O', 'raw', f'{image}.raw'])

    # Montage de l'image de disque brut
    partitions = subprocess.check_output(['parted', '-s', f'{image}.raw', 'unit', 'b', 'print'])
    partition_info = partitions.decode('utf-8').split('\n')[2:-2]
    for partition in partition_info:
        start = partition.split()[1][:-1]
        size = partition.split()[2][:-1]
        subprocess.run([
            'sudo',
            'mount',
            '-o',
            f'loop,ro,offset={start}',
            f'{image}.raw',
            './mnt',
        ])

    # Création d'une archive tarball de la partition montée
    subprocess.run(['tar', '-C', 'mnt', '-czf', f'{nom_image}.tar.gz', '.'])

    # Importation de l'archive tarball dans Docker
    subprocess.run(['docker', 'import', f'{nom_image}.tar.gz', f'{nom_image}:1.0'])