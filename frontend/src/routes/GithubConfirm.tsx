import { Heading, Spinner, Text, useToast, VStack } from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { githubLogIn } from "../api";

export default function GithubConfirm() {
	const { search } = useLocation();
	const toast = useToast();
	const queryClient = useQueryClient();
	const navigate = useNavigate();

	// FIX 1: Use the `useMutation` hook to handle the login API call.
	// This provides onSuccess, onError, and pending states automatically.
	const mutation = useMutation({
		mutationFn: githubLogIn,
		onSuccess: () => {
			// This code runs only when the API call is successful.
			toast({
				status: "success",
				title: "Welcome!",
				position: "bottom-right",
				description: "Happy to have you back!",
			});
			// FIX 3: Update refetchQueries to the recommended v5 object syntax.
			queryClient.refetchQueries({ queryKey: ["me"] });
			navigate("/");
		},
		// FIX 2: Add an onError callback to handle login failures gracefully.
		onError: () => {
			toast({
				status: "error",
				title: "Login Failed",
				position: "bottom-right",
				description: "Something went wrong, please try again.",
			});
			navigate("/");
		},
	});

	useEffect(() => {
		// This effect runs once when the component mounts.
		const params = new URLSearchParams(search);
		const code = params.get("code");
		if (code) {
			// It triggers the mutation with the code from the URL.
			mutation.mutate(code);
		}
	}, []); // Empty dependency array ensures this runs only once.

	return (
		<VStack justifyContent={"center"} mt={40}>
			<Heading>Processing log in...</Heading>
			<Text>Don't go anywhere.</Text>
			<Spinner size="lg" />
		</VStack>
	);
}
