import pyopencl as cl

print("Version de PyOpenCL : " + cl.VERSION_TEXT)
print("Version de OpenCL : " + ".".join(map(str, cl.get_cl_header_version())) + "\n")
print("Vérification des périphériques OpenCL :")
print("---------------------------------------\n")

platforms = cl.get_platforms()
for platorm in platforms:
    print("Version de OpenCL : " + platorm.version)
    devices = platorm.get_devices(cl.device_type.ALL)
    print("\nExtensions supportées de OpenCL : " + platorm.extensions)

    print("\nCaractéristiques techniques :")
    print("-----------------------------\n")
    for dev in devices:
        sizes = (
                ("Fabricant", str(dev.vendor)),
                ("Modèle", str(dev.name)),
                ("Version", str(dev.version)),
                ("Fréquence", str(dev.max_clock_frequency)),
                ("Mémoire", str(dev.global_mem_size)),
                ("Profil", str(dev.profile)),
                ("Type", str(cl.device_type.to_string(dev.type))),
                ("Memory (local)", str(dev.local_mem_size)),
                ("Mem cache size (global)", str(dev.global_mem_cache_size)),
                ("Mem cache type (global)", str(dev.global_mem_cache_type)),
                ("Execution capabilities", str(bool(dev.execution_capabilities))),
                ("Error correction support", str(bool(dev.error_correction_support))),
                ("Address bits", str(dev.address_bits)),
                ("Max compute units", str(dev.max_compute_units)),
                ("Max work item dims", str(dev.max_work_item_dimensions)),
                ("Max work item size", str(dev.max_work_item_sizes)),
                ("Max work group size", str(dev.max_work_group_size)),
                ("Max mem alloc size", str(dev.max_mem_alloc_size)),
                ("Max samplers", str(dev.max_samplers)),
                ("Mem base addr align", str(dev.mem_base_addr_align)),
                ("Single FP config", str(bool(dev.single_fp_config))),
                ("Double FP config", str(bool(dev.double_fp_config))),
                ("Compiler available", str(bool(dev.compiler_available))),
                ("Built in kernels", str(bool(dev.built_in_kernels))),
                ("Linker available", str(bool(dev.linker_available)))
        )

        for nom, size in sizes:
            print("{0:<30} : {1:<20}".format(nom, size))
