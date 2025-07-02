import { FaAirbnb, FaMoon, FaSun } from "react-icons/fa";
import {
	Avatar,
	Box,
	Button,
	HStack,
	IconButton,
	LightMode,
	Menu,
	MenuButton,
	MenuItem,
	MenuList,
	Stack,
	ToastId,
	useColorMode,
	useColorModeValue,
	useDisclosure,
	useToast,
} from "@chakra-ui/react";
import { Link } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignUpModal from "./SignUpModal";
import useUser from "../lib/useUser";
import { logOut } from "../api";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef } from "react";

export default function Header() {
	const { userLoading, isLoggedIn, user } = useUser();
	const {
		isOpen: isLoginOpen,
		onClose: onLoginClose,
		onOpen: onLoginOpen,
	} = useDisclosure();
	const {
		isOpen: isSignUpOpen,
		onClose: onSignUpClose,
		onOpen: onSignUpOpen,
	} = useDisclosure();
	const { toggleColorMode } = useColorMode();
	const logoColor = useColorModeValue("red.500", "red.200");
	const Icon = useColorModeValue(FaMoon, FaSun);
	const toast = useToast();
	const queryClient = useQueryClient();
	const toastId = useRef<ToastId>();
	const mutation = useMutation({
		// Assign the logOut function to the mutationFn property
		mutationFn: logOut,

		onMutate: () => {
			toastId.current = toast({
				title: "Logging out...",
				description: "Sad to see you go...",
				status: "loading",
				duration: 10000,
				position: "bottom-right",
			});
		},
		onSuccess: () => {
			if (toastId.current) {
				// It's good practice to use the object syntax for refetchQueries in v5
				queryClient.refetchQueries({ queryKey: ["me"] });
				toast.update(toastId.current, {
					status: "success",
					title: "Done!",
					description: "See you later!",
				});
			}
		},
	});
	const onLogOut = async () => {
		mutation.mutate();
	};
	return (
		<Stack
			justifyContent={"space-between"}
			alignItems="center"
			py={5}
			px={40}
			direction={{
				sm: "column",
				md: "row",
			}}
			spacing={{
				sm: 4,
				md: 0,
			}}
			borderBottomWidth={1}
		>
			<Box color={logoColor}>
				<Link to={"/"}>
					<FaAirbnb size={"48"} />
				</Link>
			</Box>
			<HStack spacing={2}>
				<IconButton
					onClick={toggleColorMode}
					variant={"ghost"}
					aria-label="Toggle dark mode"
					icon={<Icon />}
				/>
				{!userLoading ? (
					!isLoggedIn ? (
						<>
							<Button onClick={onLoginOpen}>Log in</Button>
							<LightMode>
								<Button onClick={onSignUpOpen} colorScheme={"red"}>
									Sign up
								</Button>
							</LightMode>
						</>
					) : (
						<Menu>
							<MenuButton>
								<Avatar name={user?.username} src={user?.avatar} size={"md"} />
							</MenuButton>
							<MenuList>
								{user?.is_host ? (
									<Link to="/rooms/upload">
										<MenuItem>Upload room</MenuItem>
									</Link>
								) : null}
								<MenuItem onClick={onLogOut}>Log out</MenuItem>
							</MenuList>
						</Menu>
					)
				) : null}
			</HStack>
			<LoginModal isOpen={isLoginOpen} onClose={onLoginClose} />
			<SignUpModal isOpen={isSignUpOpen} onClose={onSignUpClose} />
		</Stack>
	);
}