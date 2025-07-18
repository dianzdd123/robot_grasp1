from setuptools import find_packages, setup

package_name = 'vision_ai'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    extras_require={
        'test': ['pytest'],
    },
    zip_safe=True,
    maintainer='qi',
    maintainer_email='qi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'scan_planner_node = vision_ai.scan_planner_node:main',
            'scan_executor_node = vision_ai.scan_executor_node:main',
            'smart_stitcher_node = vision_ai.smart_stitcher_node:main',
            'gui_config_node = vision_ai.gui_config_node:main',
            'detection_node = vision_ai.detection_node:main',
            # 'tracking_node = vision_ai.tracking_node:main',
            # 'static_grasp_node = vision_ai.static_grasp_node:main',
        ],
    },
)

