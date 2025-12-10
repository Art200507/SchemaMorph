(function () {
    const canvas = document.getElementById("futuristic-canvas");
    if (!canvas || typeof THREE === "undefined") {
        return;
    }

    const renderer = new THREE.WebGLRenderer({
        canvas,
        alpha: true,
        antialias: true,
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
        45,
        window.innerWidth / window.innerHeight,
        0.1,
        100
    );
    camera.position.set(0, 0, 5.5);

    // Lighting setup
    const ambient = new THREE.AmbientLight(0xffffff, 0.35);
    scene.add(ambient);

    const colors = [0x8b5cf6, 0x7c3aed, 0xf472b6];
    const pointOffsets = [
        [4, 3, 2],
        [-3, -2, 4],
        [0, 4, -3],
    ];
    pointOffsets.forEach((offset, idx) => {
        const light = new THREE.PointLight(colors[idx], 1.5, 50);
        light.position.set(...offset);
        scene.add(light);
    });

    const rimLight = new THREE.DirectionalLight(0xc4b5fd, 1.5);
    rimLight.position.set(-5, 5, 5);
    scene.add(rimLight);

    // Create blob mesh
    const geometry = new THREE.IcosahedronGeometry(1.6, 8);
    const material = new THREE.MeshPhysicalMaterial({
        color: 0x8b5cf6,
        metalness: 0.35,
        roughness: 0.1,
        transmission: 0.95,
        thickness: 2.0,
        clearcoat: 1,
        clearcoatRoughness: 0.1,
        opacity: 0.95,
        transparent: true,
    });
    const blob = new THREE.Mesh(geometry, material);
    scene.add(blob);

    const wireframe = new THREE.LineSegments(
        new THREE.WireframeGeometry(geometry),
        new THREE.LineBasicMaterial({
            color: 0xd8b4fe,
            transparent: true,
            opacity: 0.45,
        })
    );
    blob.add(wireframe);

    // cache original positions for wobble animation
    const positions = geometry.attributes.position;
    const initialPositions = positions.array.slice();

    const clock = new THREE.Clock();

    function animate() {
        const elapsed = clock.getElapsedTime();

        for (let i = 0; i < positions.count; i++) {
            const ix = i * 3;
            const iy = ix + 1;
            const iz = ix + 2;
            const offset = i * 0.15;
            const wobble = Math.sin(elapsed * 1.4 + offset) * 0.04;

            positions.array[ix] = initialPositions[ix] + wobble;
            positions.array[iy] =
                initialPositions[iy] +
                Math.cos(elapsed * 1.7 + offset) * 0.04;
            positions.array[iz] =
                initialPositions[iz] +
                Math.sin(elapsed * 1.1 + offset) * 0.04;
        }
        positions.needsUpdate = true;
        geometry.computeVertexNormals();

        blob.rotation.x = Math.sin(elapsed * 0.4) * 0.3;
        blob.rotation.y = elapsed * 0.4;

        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    }

    function handleResize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        renderer.setSize(width, height);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
    }

    window.addEventListener("resize", handleResize);
    animate();
})();
